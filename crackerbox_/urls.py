from django.urls import path

from . import views

urlpatterns = [
    path("", views.quizzer_home, name="quizzer_home"),
    path("quizzer", views.copy_paste_quizzer, name="copyPaste"),
    path("list", views.user_document_list, name="list"),
    path("upload/", views.PdfUpload.as_view(), name="upload_pdf"),
    path("create_test/", views.upload_test_view, name="create_test"),
    path(
        "create_quizzer_test/",
        views.CreateQuizzerTest.as_view(),
        name="api_create_test",
    ),
    path(
        "save_result/", views.SaveResult.as_view(), name="save_quizzer_result"
    ),
    path("<slug:slug>/", views.pdf_, name="pdf_detail"),
    path("read/<slug:slug>/", views.pdf_view, name="read_pdf"),
    path(
        "documents/<uuid:unique_id>",
        views.document_detail_view,
        name="document",
    ),
    path("results/<uuid:unique_id>", views.result_view, name="results",),
]
