from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from .utils import unique_slug_generator
from django.conf import settings
from annoying.functions import get_object_or_None

from user_profile.models import Profile


class Question(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="m_question",
        on_delete=models.CASCADE,
    )
    difficulty = models.CharField(
        max_length=10,
        choices=(("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")),
    )
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )
    question = models.CharField(max_length=160)
    option1 = models.CharField(max_length=64)
    option2 = models.CharField(max_length=64)
    option3 = models.CharField(max_length=64)
    option4 = models.CharField(max_length=64)
    ans = models.CharField(max_length=1)
    docfile = models.FileField(
        upload_to="documents/MChoice/", blank=True, null=True
    )
    created_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.creator}"


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def r_post_save_receiver(sender, instance, created, *args, **kwargs):
    user_profile = get_object_or_None(Profile, user=instance.creator)

    if not instance.edited:
        user_profile.modify_reputation(2)
        instance.edited = True
        instance.save()


pre_save.connect(rl_pre_save_receiver, sender=Question)
post_save.connect(r_post_save_receiver, sender=Question)


class Category(models.Model):
    name = models.CharField(
        max_length=50, blank=False, null=False, default="", unique=True
    )

    def __str__(self):
        return self.name


class Comments(models.Model):
    text = models.CharField(
        max_length=180, blank=False, null=False, default=""
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="m_comments",
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )

    def __str__(self):
        return f"{self.text} by {self.creator}"


class Vote(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="m_vote",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    value = models.BooleanField()

    class Meta:
        unique_together = (("creator", "question"),)
