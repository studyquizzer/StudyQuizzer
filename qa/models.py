import datetime

from annoying.fields import AutoOneToOneField
from annoying.functions import get_object_or_None
from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from hitcount.models import HitCountMixin
from taggit.managers import TaggableManager

from martor.models import MartorField

from .models_utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


# class UserQAProfile(models.Model):
#     """Model class to define a User profile for the app, directly linked
#     to the core Django user model."""

#     user = AutoOneToOneField(
#         settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
#     )
#     points = models.IntegerField(default=0)
#     # The additional attributes we wish to include.
#     website = models.URLField(blank=True)

#     slug = models.SlugField(max_length=200)

#     def modify_reputation(self, added_points):
#         """Core function to modify the reputation of the user profile."""
#         self.points = F("points") + added_points
#         self.save()

#     def __str__(self):  # pragma: no cover
#         return self.user.username

#     def get_absolute_url(self):
#         return reverse("qa_profile", args=[str(self.slug)])


# def rl_post_save_receiver1(sender, instance, *args, **kwargs):
#     # slg = get_object_or_None(settings.AUTH_USER_MODEL, id= instance.user.id)
#     instance.slug = instance.user.profile.slug


# post_save.connect(rl_post_save_receiver1, sender=UserQAProfile)


class Question(models.Model, HitCountMixin):
    """Model class to contain every question in the forum"""

    slug = models.SlugField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, blank=False)
    description = MartorField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    tags = TaggableManager()
    reward = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    closed = models.BooleanField(default=False)
    close = models.BooleanField(default=False)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    flag = models.ForeignKey(
        "Flag", blank=True, null=True, on_delete=models.SET_NULL
    )
    flag_count = models.ManyToManyField(
        User, blank=True, related_name="flagger_question"
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.slug
            try:
                points = settings.QA_SETTINGS["reputation"]["CREATE_QUESTION"]

            except KeyError:
                points = 0

            self.user.profile.modify_reputation(points)

        self.total_points = self.positive_votes - self.negative_votes
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def in_days(self):
        t1 = datetime.datetime.now - self.pub_date
        if t1.total_seconds() > 86400:
            return True
        else:
            return False

    def flag_spam(self, user_):
        spam = get_object_or_None(Flag, type="s")
        self.flag = spam
        self.flag_count.add(user_)
        self.save()

    def flag_inapp(self, user_):
        inapp = get_object_or_None(Flag, type="i")
        self.flag = inapp
        self.flag_count.add(user_)
        self.save()

    def get_absolute_url(self):
        return reverse("qa_detail", kwargs={"pk": self.pk})


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=Question)


class Answer(models.Model):
    """Model class to contain every answer in the forum and to link it
    to the proper question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = MartorField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    updated = models.DateTimeField("date updated", auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    answer = models.BooleanField(default=False)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    flag = models.ForeignKey(
        "Flag", blank=True, null=True, on_delete=models.SET_NULL
    )
    flag_count = models.ManyToManyField(
        User, blank=True, related_name="flagger_answer"
    )

    def save(self, *args, **kwargs):
        try:
            points = settings.QA_SETTINGS["reputation"]["CREATE_ANSWER"]

        except KeyError:
            points = 0

        self.user.profile.modify_reputation(points)
        self.total_points = self.positive_votes - self.negative_votes
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):  # pragma: no cover
        return self.answer_text

    def in_days(self):
        t1 = datetime.datetime.now - self.pub_date
        if t1.total_seconds() > 86400:
            return True
        else:
            return False

    def flag_spam(self, user_):
        spam = get_object_or_None(Flag, type="s")
        self.flag = spam
        self.flag_count.add(user_)
        self.save()

    def flag_inapp(self, user_):
        inapp = get_object_or_None(Flag, type="i")
        self.flag = inapp
        self.flag_count.add(user_)
        self.save()

    class Meta:
        ordering = ["-answer", "-pub_date"]


class VoteParent(models.Model):
    """Abstract model to define the basic elements to every single vote."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    value = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AnswerVote(VoteParent):
    """Model class to contain the votes for the answers."""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "answer"),)


class QuestionVote(VoteParent):
    """Model class to contain the votes for the questions."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "question"),)


class BaseComment(models.Model):
    """Abstract model to define the basic elements to every single comment."""

    pub_date = models.DateTimeField("date published", auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    flag = models.ForeignKey(
        "Flag", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def __str__(self):  # pragma: no cover
        return self.comment_text

    def flag_spam(self, user_):
        spam = get_object_or_None(Flag, type="s")
        self.flag = spam
        self.flag_count.add(user_)
        self.save()

    def flag_inapp(self, user_):
        inapp = get_object_or_None(Flag, type="i")
        self.flag = inapp
        self.flag_count.add(user_)
        self.save()


class AnswerComment(BaseComment):
    """Model class to contain the comments for the answers."""

    comment_text = MartorField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    flag_count = models.ManyToManyField(
        User, blank=True, related_name="flagger_answer_comment"
    )

    def save(self, *args, **kwargs):
        try:
            points = settings.QA_SETTINGS["reputation"][
                "CREATE_ANSWER_COMMENT"
            ]

        except KeyError:
            points = 0

        self.user.profile.modify_reputation(points)
        super(AnswerComment, self).save(*args, **kwargs)


class QuestionComment(BaseComment):
    """Model class to contain the comments for the questions."""

    comment_text = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    flag_count = models.ManyToManyField(
        User, blank=True, related_name="flagger_question_comment"
    )

    def save(self, *args, **kwargs):
        try:
            points = settings.QA_SETTINGS["reputation"][
                "CREATE_QUESTION_COMMENT"
            ]

        except KeyError:
            points = 0

        self.user.profile.modify_reputation(points)
        super(QuestionComment, self).save(*args, **kwargs)


class Flag(models.Model):
    flag_choices = (("s", "spam"), ("i", "inappropriate"))

    type = models.CharField(max_length=1, choices=flag_choices)

    def __str__(self):
        return self.type
