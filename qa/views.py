import datetime
import operator
from functools import reduce

from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView, View
from hitcount.views import HitCountDetailView
from taggit.models import Tag, TaggedItem

from crackerbox_.models import AllDocumentCount, Document
from qa.models import (
    Answer,
    AnswerComment,
    AnswerVote,
    Question,
    QuestionComment,
    QuestionVote,
)
from users.models import User
from user_profile.models import Profile

from .forms import QuestionForm
from .mixins import AuthorRequiredMixin, LoginRequired
from .utils import question_score


class profile_checkMixin(UserPassesTestMixin):
    login_url = "/profile"

    permission_denied_message = "Nothing"

    message = "Sorry you have to complete you profile to do that."

    def handle_no_permission(self):
        messages.success(self.request, self.message)
        return redirect("make_profiled")

    def test_func(self):
        if self.request.user.profiled:
            return True
        return False


def profile_check(user):
    return user.profiled


try:
    qa_messages = (
        "django.contrib.messages" in settings.INSTALLED_APPS
        and settings.QA_SETTINGS["qa_messages"]
    )

except AttributeError:  # pragma: no cover
    qa_messages = False

if qa_messages:
    from django.contrib import messages

"""Dear maintainer:

Once you are done trying to 'optimize' this routine, and have realized what a
terrible mistake that was, please increment the following counter as a warning
to the next guy:

total_hours_wasted_here = 2
"""


class AnswerQuestionView(LoginRequired, profile_checkMixin, View):
    """
    View to select an answer as the satisfying answer to the question,
    validating than the user who created que
    question is the only one allowed to make those changes.
    """

    model = Answer

    def post(self, request, answer_id):
        answer = get_object_or_404(self.model, pk=answer_id)
        if answer.question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question."
            )

        else:
            answer.question.answer_set.update(answer=False)
            answer.answer = True
            answer.save()

            try:
                points = settings.QA_SETTINGS["reputation"]["ACCEPT_ANSWER"]

            except KeyError:
                points = 0

            qa_user = Profile.objects.get(user=answer.user)
            qa_user.modify_reputation(points)

        next_url = request.POST.get("next", "")
        if next_url != "":
            return redirect(next_url)

        else:
            return redirect(reverse("qa_index"))


class CloseQuestionView(LoginRequired, View):
    """View to
    mark the question as closed, validating than the user who created que
    question is the only one allowed to make those changes.
    """

    model = Question

    def post(self, request, question_id):
        question = get_object_or_404(self.model, pk=question_id)
        if question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question."
            )
        else:
            if not question.close:
                question.close = True

            else:
                raise ValidationError("Sorry, this question is already closed")

            question.save()

        next_url = request.POST.get("next", "")
        if next_url != "":
            return redirect(next_url)

        else:
            return redirect(reverse("qa_index"))


class QuestionIndexView(ListView):
    """CBV to render the index view
    """

    model = Question
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/index.html"
    ordering = "-pub_date"

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionIndexView, self).get_context_data(
            *args, **kwargs
        )
        noans = (
            Question.objects.order_by("-pub_date")
            .filter(answer__isnull=True)
            .select_related("user")
            .annotate(
                num_answers=Count("answer", distinct=True),
                num_question_comments=Count("questioncomment", distinct=True),
            )
        )
        context["totalcount"] = Question.objects.count()
        context["anscount"] = Answer.objects.count()
        paginator = Paginator(noans, 10)
        page = self.request.GET.get("noans_page")

        try:
            noans = paginator.page(page)

        except PageNotAnInteger:
            noans = paginator.page(1)

        except EmptyPage:  # pragma: no cover
            noans = paginator.page(paginator.num_pages)

        context["totalnoans"] = paginator.count
        context["noans"] = noans
        context["reward"] = Question.objects.order_by("-reward").filter(
            reward__gte=1
        )[:10]

        question_contenttype = ContentType.objects.get_for_model(Question)
        items = TaggedItem.objects.filter(content_type=question_contenttype)
        context["tags"] = (
            Tag.objects.filter(taggit_taggeditem_items__in=items)
            .order_by("-id")
            .distinct()[:10]
        )

        return context

    def get_queryset(self):
        queryset = (
            super(QuestionIndexView, self)
            .get_queryset()
            .select_related("user")
            .annotate(
                num_answers=Count("answer", distinct=True),
                num_question_comments=Count("questioncomment", distinct=True),
            )
        )
        return queryset


class QuestionsSearchView(QuestionIndexView):
    """
    Display a ListView page inherithed from the QuestionIndexView filtered by
    the search query and sorted by the different elements aggregated.
    """

    def get_queryset(self):
        result = super(QuestionsSearchView, self).get_queryset()
        query = self.request.GET.get("word", "")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.and_, (Q(title__icontains=q) for q in query_list)
                )
                | reduce(
                    operator.and_,
                    (Q(description__icontains=q) for q in query_list),
                )
            )

        return result

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionsSearchView, self).get_context_data(
            *args, **kwargs
        )
        context["totalcount"] = Question.objects.count
        context["anscount"] = Answer.objects.count
        context["noans"] = Question.objects.order_by("-pub_date").filter(
            answer__isnull=True
        )[:10]
        context["reward"] = Question.objects.order_by("-reward").filter(
            reward__gte=1
        )[:10]
        return context


class QuestionsByTagView(ListView):
    """View to call all the questions clasiffied under one specific tag.
    """

    model = Question
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/index.html"

    def get_queryset(self, **kwargs):
        return Question.objects.filter(tags__slug=self.kwargs["tag"])

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionsByTagView, self).get_context_data(
            *args, **kwargs
        )
        context["active_tab"] = self.request.GET.get("active_tab", "latest")
        tabs = ["latest", "unans", "reward"]
        context["active_tab"] = (
            "latest"
            if context["active_tab"] not in tabs
            else context["active_tab"]
        )
        context["totalcount"] = Question.objects.count
        context["anscount"] = Answer.objects.count
        context["noans"] = Question.objects.order_by("-pub_date").filter(
            tags__name__contains=self.kwargs["tag"], answer__isnull=True
        )[:10]
        context["reward"] = Question.objects.order_by("-reward").filter(
            tags__name__contains=self.kwargs["tag"], reward__gte=1
        )[:10]
        context["totalnoans"] = len(context["noans"])
        return context


class CreateQuestionView(LoginRequired, profile_checkMixin, CreateView):
    """
    View to handle the creation of a new question
    """

    template_name = "qa/create_question.html"
    message = _("Thank you! your question has been created.")
    form_class = QuestionForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse("qa_index")


class UpdateQuestionView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question
    """

    template_name = "qa/update_question.html"
    model = Question
    pk_url_kwarg = "question_id"
    fields = ["title", "description", "tags"]

    def get_success_url(self):
        question = self.get_object()
        return reverse("qa_detail", kwargs={"pk": question.pk})


class CreateAnswerView(LoginRequired, profile_checkMixin, CreateView):
    """
    View to create new answers for a given question
    """

    template_name = "qa/create_answer.html"
    model = Answer
    fields = ["answer_text"]
    message = _("Thank you! your answer has been posted.")

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse("qa_detail", kwargs={"pk": self.kwargs["question_id"]})


class UpdateAnswerView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question answer
    """

    template_name = "qa/update_answer.html"
    model = Answer
    pk_url_kwarg = "answer_id"
    fields = ["answer_text"]

    def get_success_url(self):
        answer = self.get_object()
        return reverse("qa_detail", kwargs={"pk": answer.question.pk})


class CreateAnswerCommentView(LoginRequired, profile_checkMixin, CreateView):
    """
    View to create new comments for a given answer
    """

    template_name = "qa/create_comment.html"
    model = AnswerComment
    fields = ["comment_text"]
    message = _("Thank you! your comment has been posted.")

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs["answer_id"]
        return super(CreateAnswerCommentView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        question_pk = Answer.objects.get(
            id=self.kwargs["answer_id"]
        ).question.pk
        return reverse("qa_detail", kwargs={"pk": question_pk})


class CreateQuestionCommentView(LoginRequired, profile_checkMixin, CreateView):
    """
    View to create new comments for a given question
    """

    template_name = "qa/create_comment.html"
    model = QuestionComment
    fields = ["comment_text"]
    message = _("Thank you! your comment has been posted.")

    def form_valid(self, form):
        """
        Creates the required relationship between question
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super(CreateQuestionCommentView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse("qa_detail", kwargs={"pk": self.kwargs["question_id"]})


class UpdateQuestionCommentView(
    LoginRequired, AuthorRequiredMixin, UpdateView
):
    """
    Updates the comment question
    """

    template_name = "qa/create_comment.html"
    model = QuestionComment
    pk_url_kwarg = "comment_id"
    fields = ["comment_text"]

    def get_success_url(self):
        question_comment = self.get_object()
        return reverse(
            "qa_detail", kwargs={"pk": question_comment.question.pk}
        )


class UpdateAnswerCommentView(UpdateQuestionCommentView):
    """
    Updates the comment answer
    """

    model = AnswerComment

    def get_success_url(self):
        answer_comment = self.get_object()
        return reverse(
            "qa_detail", kwargs={"pk": answer_comment.answer.question.pk}
        )


class QuestionDetailView(HitCountDetailView):
    """
    View to call a question and to render all the details about that question.
    """

    model = Question
    template_name = "qa/detail_question.html"
    context_object_name = "question"
    slug_field = "slug"
    try:
        count_hit = settings.QA_SETTINGS["count_hits"]

    except KeyError:
        count_hit = True

    def get_context_data(self, **kwargs):
        my_object = self.get_object()
        slug = my_object.slug
        q = get_object_or_None(Question, slug=slug)
        answers = self.object.answer_set.all().order_by("pub_date")
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        if q:
            context["time"] = get_duration(q)
            context["day"] = get_day(q)
        context["last_comments"] = self.object.questioncomment_set.order_by(
            "pub_date"
        )[:5]
        context["answers"] = list(
            answers.select_related("user")
            .select_related("user__profile")
            .annotate(answercomment_count=Count("answercomment"))
        )
        return context

    def get(self, request, **kwargs):
        my_object = self.get_object()
        slug = kwargs.get("slug", "")
        if slug != my_object.slug:
            kwargs["slug"] = my_object.slug
            return redirect(reverse("qa_detail", kwargs=kwargs))

        else:
            return super(QuestionDetailView, self).get(request, **kwargs)

    def get_object(self):
        question = super(QuestionDetailView, self).get_object()
        return question


class ParentVoteView(View):
    """Base class to create a vote for a given model (question/answer)
    """

    model = None
    vote_model = None

    def get_vote_kwargs(self, user, vote_target):
        """
        This takes the user and the vote and adjusts the kwargs
        depending on the used model.
        """
        object_kwargs = {"user": user}
        if self.model == Question:
            target_key = "question"

        elif self.model == Answer:
            target_key = "answer"

        else:
            raise ValidationError("Not a valid model for votes")

        object_kwargs[target_key] = vote_target
        return object_kwargs

    def post(self, request, object_id):
        vote_target = get_object_or_404(self.model, pk=object_id)
        if vote_target.user == request.user:
            message = "Sorry, Voting for your post is not allowed."
            messages.warning(self.request, message)

            next_url = request.POST.get("next", "")
            if next_url != "":
                return redirect(next_url)

            else:
                return redirect(reverse("qa_index"))

        else:
            upvote = request.POST.get("upvote", None) is not None
            object_kwargs = self.get_vote_kwargs(request.user, vote_target)
            vote, created = self.vote_model.objects.get_or_create(
                defaults={"value": upvote}, **object_kwargs
            )
            print(vote, created)
            if created:
                vote_target.user.profile.points += 1 if upvote else -1
                if upvote:
                    vote_target.positive_votes += 1

                else:
                    vote_target.negative_votes += 1

            else:
                if vote.value == upvote:
                    vote.delete()
                    vote_target.user.profile.points += -1 if upvote else 1
                    if upvote:
                        vote_target.positive_votes -= 1

                    else:
                        vote_target.negative_votes -= 1

                else:
                    vote_target.user.profile.points += 2 if upvote else -2
                    vote.value = upvote
                    vote.save()
                    if upvote:
                        vote_target.positive_votes += 1
                        vote_target.negative_votes -= 1

                    else:
                        vote_target.negative_votes += 1
                        vote_target.positive_votes -= 1

            vote_target.user.profile.save()
            if self.model == Question:
                vote_target.reward = question_score(vote_target)

            if self.model == Answer:
                vote_target.question.reward = question_score(
                    vote_target.question
                )
                vote_target.question.save()

            vote_target.save()

        next_url = request.POST.get("next", "")
        if next_url != "":
            return redirect(next_url)

        else:
            return redirect(reverse("qa_index"))


class AnswerVoteView(ParentVoteView):
    """
    Class to upvote answers
    """

    model = Answer
    vote_model = AnswerVote


class QuestionVoteView(ParentVoteView):
    """
    Class to upvote questions
    """

    model = Question
    vote_model = QuestionVote


def profile(request, slug):
    """
        Resolve document iterations because of hit count.
    """
    user_ob = get_user_model().objects.get(profile__slug=slug)
    user = Profile.objects.get(user=user_ob)
    tag_ = getTag(user_ob)
    tCount = 0
    questions = Question.objects.filter(user=user_ob)
    date_joined = get_date_joined(user_ob)
    documents = Document.objects.filter(owner=request.user)
    for obj in questions:
        viewX = obj.hit_count.hits
        tCount += viewX
    answer = Answer.objects.filter(user=user_ob).count()
    context = {
        "user": user,
        "question_count": questions.count,
        "answer": answer,
        "tCount": tCount,
        "tag_": tag_,
        "date_joined": date_joined,
        "documents": documents,
    }
    return render(request, "qa/profile_.html", context)


def base_home(request):
    time = datetime.datetime.now().year
    questions = get_object_or_None(AllDocumentCount, name="Document_count")

    if questions is not None:
        questions = questions.count
    context = {"time": time, "questions": questions}
    return render(request, "home.html", context)


def flag_question_spam(request, id):
    try:
        question = Question.objects.get(id=id)
        question.flag_spam(request.user)
    except Question.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_question_inapp(request, id):
    try:
        question = Question.objects.get(id=id)
        question.flag_inapp(request.user)
    except Question.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_answer_spam(request, id):
    try:
        answer = Answer.objects.get(id=id)
        answer.flag_spam(request.user)
    except Answer.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_answer_inapp(request, id):
    try:
        answer = Answer.objects.get(id=id)
        answer.flag_inapp(request.user)
    except Answer.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_answercomment_spam(request, id):
    try:
        comment = AnswerComment.objects.get(id=id)
        comment.flag_spam(request.user)
    except AnswerComment.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_answercomment_inapp(request, id):
    try:
        comment = AnswerComment.objects.get(id=id)
        comment.flag_inapp(request.user)
    except AnswerComment.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_questioncomment_spam(request, id):
    try:
        comment = QuestionComment.objects.get(id=id)
        comment.flag_spam(request.user)
    except QuestionComment.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_question.html", {})


def flag_questioncomment_inapp(request, id):
    try:
        comment = QuestionComment.objects.get(id=id)
        comment.flag_inapp(request.user)
    except QuestionComment.DoesNotExist:
        raise Http404("Error 404")
    return render(request, "flag_answer.html", {})


def getTag(user: str) -> list:
    q = Question.objects.filter(user=user)
    tags = []
    c = 0
    if q.exists():
        for obj in q:
            for tg in obj.tags.all():
                tags.append(tg)
                c += 1
                if c == 5:
                    break
    # print(tags)
    return tags


def get_date_joined(user):
    date = user.timestamp.strftime("%B %d, %Y, %I:%M %p")
    return date


def get_similar_reader(user) -> list:
    my_book = user.book_category
    if my_book is not None:
        similar_readers = User.objects.filter(book_category=my_book).exclude(
            username=user.username
        )
        return similar_readers
    else:
        return []


def get_duration(q):
    now_aware = timezone.now()
    time_diffH = 0
    time_diffM = 0
    time_elapsed = now_aware - q.pub_date
    timeX = time_elapsed.total_seconds()
    if 3600 <= timeX < 86400:
        time_diffH = int(timeX / 3600)
    elif timeX < 3600:
        time_diffM = int(timeX / 60) % 60

    time = ""
    if (time_diffH != 0) and (time_diffM == 0):
        if time_diffH < 2:
            time = f"{time_diffH} hour ago"
        else:
            time = f"{time_diffH} hours ago"
        return time
    else:
        if time_diffM < 2:
            time = f"{time_diffM} minute ago"
        else:
            time = f"{time_diffM} minutes ago"
        return time


def get_day(q):
    time = q.pub_date
    day = time.strftime("%b %d'%y")
    time_ = time.strftime("%I:%M %p")
    day = f"{day} at {time_}"
    return day
