from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# app_name = 'rest'

# router = routers.DefaultRouter()
# router.register('documents',views.DocumentList.as_view()
# )

urlpatterns = [
    path("", views.api_root),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("testlogin/", views.TestLogin.as_view(), name="test-login"),
    path("category/", views.CategoryCreate.as_view(), name="category-create"),
    path(
        "comments/<slug:slug>",
        views.CommentsGet.as_view(),
        name="comments-get",
    ),
    path(
        "comment-create/", views.CommentCreate.as_view(), name="comment-create"
    ),
    path("votes/<slug:slug>", views.VotesGet.as_view(), name="votes-get"),
    path("vote-create/", views.VoteCreate.as_view(), name="vote-create"),
    path(
        "MultiQuestions/<slug:slug>/<slug:Question_slug>",
        views.QuestionDetail.as_view(),
        name="MQuestionList",
    ),
    path(
        "MultiQuestions/<slug:slug>",
        views.QuestionList.as_view(),
        name="MQuestionList",
    )
    # path('users/',  views.UserList.as_view(), name='user-list'),
    # path('users/<slug:slug>',  views.UserDetail.as_view(), name='user-detail'),
    # #path('documents', include('router.urls')),
    # path('documents/', views.DocumentList.as_view(), name='document-list'),
    # path('documents/<slug:slug>', views.DocumentDetail.as_view(), name='document-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
