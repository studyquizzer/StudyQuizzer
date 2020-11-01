from annoying.functions import get_object_or_None
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, TemplateView

from user_profile.models import Profile
from users.models import User
from .models import Chat, Chatkit
from .tasks import create_chat


class ChatEligibleMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("qa_index")
        else:
            return redirect("login")

    def test_func(self, **kwargs):
        slug = self.kwargs.get("slug")
        user2 = get_object_or_None(User, username=slug)

        if slug == self.request.user.username:
            return False
        if user2 is None:
            return False

        book = self.request.user.book
        book2 = user2.book

        if book is not None and book2 is not None:
            if book == book2:
                return True
        return False


class Message(LoginRequiredMixin, ChatEligibleMixin, TemplateView):
    template_name = "thread.html"
    success_url = "./"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")
        user1_already_exist = False
        user2_already_exist = False

        can_chat = Chat.objects.filter(user1=self.request.user).filter(
            user2__username=slug
        )
        can_chat_reverse = Chat.objects.filter(user2=self.request.user).filter(
            user1__username=slug
        )
        user_2 = get_object_or_None(User, username=slug)

        # possible bug if reverse exit then no need of uae11 or uae22
        user_1_as_sender = Chat.objects.filter(user1=self.request.user)
        user_1_as_reciever = Chat.objects.filter(user2=self.request.user)

        user_2_as_sender = Chat.objects.filter(user1=user_2)
        user_2_as_reciever = Chat.objects.filter(user2=user_2)

        if user_1_as_sender.exists() or user_1_as_reciever.exists():
            user1_already_exist = True

        if user_2_as_sender.exists() or user_2_as_reciever.exists():
            user2_already_exist = True

        exist = False

        if can_chat.exists():
            exist = True
            chat_obj = can_chat

        elif can_chat_reverse.exists():
            exist = True
            chat_obj = can_chat_reverse

        else:
            user = self.request.user
            chat = Chat()
            chat.user1 = user
            chat.user2 = user_2
            chat.save()
            chat_obj = chat
            create_chat(chat, user1_already_exist, user2_already_exist)

        context = super().get_context_data(**kwargs)
        other_user = get_object_or_None(
            Profile, user__username=self.kwargs.get("slug")
        )
        context["other_user"] = other_user
        context["exist"] = exist
        context["chat_obj"] = None
        if exist:
            context["chat_obj"] = chat_obj[0]
        else:
            context["chat_obj"] = chat_obj
        return context


@csrf_protect
def set_room_id(request, id):
    if request.is_ajax():
        pass
    else:
        raise Http404

    if request.method == "POST":
        room_id = request.POST["roomId"]
        chat = Chat.objects.get(id=id)
        chat.roomId = room_id
        chat.save()
        message = {"room_id": room_id}
        return JsonResponse(message)
    else:
        HttpResponseForbidden()


def send_room_id(request, id):
    if request.is_ajax():
        pass
    else:
        raise Http404

    if request.method == "GET":
        chat = Chat.objects.get(id=id)
        room_id = chat.roomId
        response_data = {"id": room_id}
        return JsonResponse(response_data)
    else:
        HttpResponseForbidden()


def get_auth_details(request):
    if request.is_ajax():
        pass
    else:
        raise Http404

    if request.method == "GET":
        instance = Chatkit.objects.all()[0]
        token_provider = instance.tokenProvider
        instance_locator = instance.instanceLocator
        response_data = {
            "tokenProvider": token_provider,
            "instanceLocator": instance_locator,
        }
        print(response_data)
        return JsonResponse(response_data)
    else:
        HttpResponseForbidden()
