import json
import random

from annoying.functions import get_object_or_None
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse, request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.edit import CreateView
from django_q.tasks import async_task
from notifications.signals import notify

from crackerbox_.helpers import generate_unique_id
from crackerbox_.models import (
    Document,
    Question,
    QuizzerRecord,
    COMPLETE,
    PROCESSING,
    ERROR,
)
from utils import get_similar_readers, unique_slug_generator

from . import forms, models


class ProfileCheckMixin(UserPassesTestMixin):
    login_url = "/profile"

    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.profiled:
            return True
        return False


def profile_check(user):
    if user.is_authenticated and user.profiled:
        return True
    return False


@login_required
@user_passes_test(profile_check, login_url="/profile")
def quizzer_home(request):
    context = {}
    return render(request, "quizzer_home.html", context)


class PdfUpload(ProfileCheckMixin, CreateView):
    model = models.Pdf
    fields = ["title", "category"]
    template_name = "pdf_upload.html"

    def form_valid(self, form):
        instance = form.save(commit=False)

        title = form.cleaned_data["title"].title()
        category = form.cleaned_data["category"]

        instance.title = title
        instance.category = category
        instance.owner = self.request.user
        instance.slug = unique_slug_generator(instance)

        self.request.user.book_title = title
        self.request.user.book_category = category

        self.request.user.save()

        similar_readers = get_similar_readers(category)
        if similar_readers:
            for user in similar_readers:
                if user == self.request.user:
                    continue

                notify.send(
                    sender=user,
                    recipient=self.request.user,
                    verb=f"Hello {self.request.user.username}, looks like we are both reading {category}. Click to chat.",
                )
                notify.send(
                    sender=self.request.user,
                    recipient=user,
                    verb=f"Hello {user.username}, looks like we are both reading {category}. Click to chat.",
                )

        return super(PdfUpload, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return models.reverse("pdf_detail", kwargs={"slug": self.object.slug})


@login_required
@user_passes_test(profile_check, login_url="/profile")
def pdf_(request, slug):
    doc = get_object_or_404(models.Pdf, slug=slug)
    context = {"doc": doc}
    return render(request, "reader.html", context)


@login_required
@user_passes_test(profile_check, login_url="/profile")
def pdf_view(request, slug):
    doc = get_object_or_404(models.Pdf, slug=slug)
    context = {"doc": doc}
    return render(request, "viewer.html", context)


@login_required
@user_passes_test(profile_check, login_url="/profile")
def copy_paste_quizzer(request):
    if request.method == "POST":
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            d_count = get_object_or_None(
                models.AllDocumentCount, name="Document_count"
            )
            if d_count is not None:
                d_count.count += 1
            else:
                d_count = models.AllDocumentCount.objects.create()
                d_count.count = 1
            d_count.save()

            text = form.cleaned_data["docText"]
            num_of_questions = form.cleaned_data["numberOfQuestions"]

            doc = form.generateDocumentObject(request.user)
            doc.owner = request.user
            doc.status = models.Document.IN_QUEUE
            doc.save()

            async_task(
                "brain.crackerbox",
                text,
                doc.unique_id,
                num_of_questions,
                task_name=f"task-{doc.unique_id}-of-{doc.owner.username}",
                hook="brain.handle_async_error",
            )
            return redirect(doc)
    else:
        form = forms.DocumentForm()
    return render(request, "copy_paste_quizzer.html", {"form": form})


class CreateQuizzerTest(ProfileCheckMixin, View):
    def post(self, request):
        data = json.loads(request.body)["data"]

        doc = Document()
        doc.title = data["title"]
        doc.unique_id = generate_unique_id()
        doc.owner = request.user
        doc.save()

        for question in data["questions"]:
            question_object = Question()
            question_object.text = question["question"]
            question_object.answer = question["answer"].title()
            question_object.doc = doc

            if question["question_type"] == "Multiple Choice":
                question_object.option1 = question["option1"]
                question_object.option2 = question["option2"]
                question_object.option3 = question["option3"]

            question_object.save()

        doc.status = COMPLETE
        doc.save()

        return HttpResponse("profile_")


@login_required
@user_passes_test(profile_check, login_url="/profile")
def user_document_list(request):
    # Load documents for the list page
    documents = models.Document.objects.filter(owner=request.user)
    # Render list page with the documents and the form
    return render(request, "list.html", {"documents": documents})


@login_required
@user_passes_test(profile_check, login_url="/profile")
def document(request, slug):
    # not sure what is going on
    # doc = get_object_or_404(models.Document, slug=slug)
    return render(request, "exam.html")


def error_404(request):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=404)


@login_required
@user_passes_test(profile_check, login_url="/profile")
def document_detail_view(request, unique_id):
    record = get_object_or_None(
        QuizzerRecord, document__unique_id=unique_id, owner=request.user
    )
    if record:
        messages.warning(request, "You've attempted this quiz already.")
        return redirect("quizzer_home")
    return render(request, "new_quizzer/quizzer.html", {"id": unique_id})


@login_required
@user_passes_test(profile_check, login_url="/profile")
def upload_test_view(request):
    return render(request, "create_test/test.html")


@login_required
@user_passes_test(profile_check, login_url="/profile")
def result_view(request, unique_id):
    result = models.QuizzerRecord.objects.filter(document__unique_id=unique_id)
    return render(request, "result.html", {"results": result})


@login_required
@user_passes_test(profile_check, login_url="/profile")
def docjson(request, id):
    doc = get_object_or_None(models.Document, unique_id=id)
    all_questions = doc.questions.all()

    json_questions = []

    for qn in all_questions:
        options = [qn.answer, qn.option1, qn.option2, qn.option3]
        random.shuffle(options)
        json_questions.append(
            {
                "text": qn.text,
                "answer": qn.answer,
                "options": options,
                "type": qn.question_type,
            }
        )
    json_doc = {"questions": json_questions, "status": doc.status}

    return JsonResponse(json_doc, safe=False)


class SaveResult(ProfileCheckMixin, View):
    def post(self, request):
        data = json.loads(request.body)

        document = Document.objects.get(unique_id=data["id"])
        record, _ = QuizzerRecord.objects.get_or_create(
            owner=request.user, document=document
        )

        record.score = data["score"]
        record.total = data["total"]
        record.save()

        return HttpResponse("result")
