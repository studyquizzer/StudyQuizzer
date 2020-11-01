from django.conf.urls import url
from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    url(r"^$", views.QuestionIndexView.as_view(), name="qa_index"),
    url(
        r"^question/(?P<pk>\d+)/$",
        views.QuestionDetailView.as_view(),
        name="qa_detail",
    ),
    url(
        r"^question/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$",
        views.QuestionDetailView.as_view(),
        name="qa_detail",
    ),
    url(
        r"^question/answer/(?P<answer_id>\d+)/$",
        views.AnswerQuestionView.as_view(),
        name="qa_answer_question",
    ),
    url(
        r"^question/close/(?P<question_id>\d+)/$",
        views.CloseQuestionView.as_view(),
        name="qa_close_question",
    ),
    url(
        r"^new-question/$",
        views.CreateQuestionView.as_view(),
        name="qa_create_question",
    ),
    url(
        r"^edit-question/(?P<question_id>\d+)/$",
        views.UpdateQuestionView.as_view(),
        name="qa_update_question",
    ),
    url(
        r"^answer/(?P<question_id>\d+)/$",
        views.CreateAnswerView.as_view(),
        name="qa_create_answer",
    ),
    url(
        r"^answer/edit/(?P<answer_id>\d+)/$",
        views.UpdateAnswerView.as_view(),
        name="qa_update_answer",
    ),
    url(
        r"^vote/question/(?P<object_id>\d+)/$",
        views.QuestionVoteView.as_view(),
        name="qa_question_vote",
    ),
    url(
        r"^vote/answer/(?P<object_id>\d+)/$",
        views.AnswerVoteView.as_view(),
        name="qa_answer_vote",
    ),
    url(
        r"^comment-answer/(?P<answer_id>\d+)/$",
        views.CreateAnswerCommentView.as_view(),
        name="qa_create_answer_comment",
    ),
    url(
        r"^comment-question/(?P<question_id>\d+)/$",
        views.CreateQuestionCommentView.as_view(),
        name="qa_create_question_comment",
    ),
    url(
        r"^comment-question/edit/(?P<comment_id>\d+)/$",
        views.UpdateQuestionCommentView.as_view(),
        name="qa_update_question_comment",
    ),
    url(
        r"^comment-answer/edit/(?P<comment_id>\d+)/$",
        views.UpdateAnswerCommentView.as_view(),
        name="qa_update_answer_comment",
    ),
    url(r"^search/$", views.QuestionsSearchView.as_view(), name="qa_search"),
    url(
        r"^tag/(?P<tag>[-\w]+)/$",
        views.QuestionsByTagView.as_view(),
        name="qa_tag",
    ),
    path("profile/<slug:slug>", views.profile, name="qa_profile"),
    # path('home/', views.home, name='home'),
    path(
        "flag_question_spam/<int:id>",
        views.flag_question_spam,
        name="flag_question_spam",
    ),
    path(
        "flag_question_inapp/<int:id>",
        views.flag_question_inapp,
        name="flag_question_inapp",
    ),
    path(
        "flag_answer_spam/<int:id>",
        views.flag_answer_spam,
        name="flag_answer_spam",
    ),
    path(
        "flag_answer_inapp/<int:id>",
        views.flag_answer_inapp,
        name="flag_answer_inapp",
    ),
    path(
        "flag_answercomment_spam/<int:id>",
        views.flag_answercomment_spam,
        name="flag_answercomment_spam",
    ),
    path(
        "flag_answercomment_inapp/<int:id>",
        views.flag_answercomment_inapp,
        name="flag_answercomment_inapp",
    ),
    path(
        "flag_questioncomment_spam/<int:id>",
        views.flag_questioncomment_spam,
        name="flag_questioncomment_spam",
    ),
    path(
        "flag_questioncomment_inapp/<int:id>",
        views.flag_questioncomment_inapp,
        name="flag_questioncomment_inapp",
    ),
    url("^markdownx/", include("markdownx.urls")),
    url(r"hitcount/", include("hitcount.urls", namespace="hitcount")),
]
