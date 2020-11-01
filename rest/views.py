from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model

from annoying.functions import get_object_or_None

from rest_framework import status, generics
from rest_framework.exceptions import ParseError, AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework.metadata import SimpleMetadata
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from crackerbox_.models import Document
from MultiChoice.models import Question as MQuestion, Vote
from MultiChoice.models import Category, Comments
from crackerbox_.tasks import process_rest
from rest.serializer import (
    MultiQuestionSerializer,
    CommentsSerializer,
    VoteSerializer,
    CategorySerializer,
    UserSerializer,
)
from user_profile.models import Profile


@api_view(("GET",))
def api_root(request, format=None):
    return Response(
        {
            "login": reverse("login", request=request, format=format),
            "logout": reverse("logout", request=request, format=format),
            "Questions": reverse(
                "MQuestionList", request=request, format=format
            ),
        }
    )


class QuestionList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MultiQuestionSerializer
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = get_object_or_None(Category, name=slug)
        queryset = MQuestion.objects.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class QuestionDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
    lookup_url_kwarg = "Question_slug"
    serializer_class = MultiQuestionSerializer

    def get_queryset(self):
        slug = self.kwargs.get("Question_slug")
        queryset = MQuestion.objects.filter(slug=slug)
        return queryset


class CommentCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentsSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class VoteCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommentsGet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
    serializer_class = CommentsSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        question = get_object_or_None(MQuestion, slug=slug)
        queryset = Comments.objects.filter(question=question)
        return queryset


class VotesGet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
    # lookup_url_kwarg = 'Question_slug'
    serializer_class = VoteSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        question = get_object_or_None(MQuestion, slug=slug)
        queryset = Vote.objects.filter(question=question)
        return queryset


class CategoryCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class UserList(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    # permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Profile.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class Login(APIView):
    class Metadata(SimpleMetadata):
        actions = {
            "POST": {
                "username": {
                    "type": "string",
                    "required": True,
                    "label": "Username",
                },
                "password": {
                    "type": "string",
                    "required": True,
                    "label": "Password",
                },
            }
        }

        def determine_metadata(self, request, view):
            metadata = super(Login.Metadata, self).determine_metadata(
                request, view
            )
            metadata["actions"] = self.actions
            return metadata

    metadata_class = Metadata
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        if "username" not in request.data:
            raise ParseError("Username not provided")
        username = request.data["username"]

        if "password" not in request.data:
            raise ParseError("Password not provided")
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Username/password invalid.")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled.")

        login(request, user)
        sz = UserSerializer(user)
        return Response(sz.data)


class Logout(APIView):
    class Metadata(SimpleMetadata):
        actions = {"POST": {}}

        def determine_metadata(self, request, view):
            metadata = super(Login.Metadata, self).determine_metadata(
                request, view
            )
            metadata["actions"] = self.actions
            return metadata

    metadata_class = Metadata

    def post(self, request, format=None):
        logout(request)
        return Response()
