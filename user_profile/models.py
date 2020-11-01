from annoying.functions import get_object_or_None
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.db.models import F

from users.models import User as user_
from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()

    sex = models.CharField(
        max_length=10, choices=(("Male", "Male"), ("Female", "Female"))
    )

    bio = models.CharField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True)

    points = models.IntegerField(default=0)
    occupation = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="profile/display", blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # follow = models.ManyToManyField( #to be reciewed
    #     "self", related_name="my_follower", symmetrical=True, blank=True,
    # )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("qa_profile", args=[str(self.slug)])

    def modify_reputation(self, added_points):
        """Core function to modify the reputation of the user profile."""
        self.points = F("points") + added_points
        self.save()

    @property
    def title(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_avatar(self):
        if self.pic:
            return self.pic
        return f"{settings.BASE_DIR}/{settings.MEDIA_URL}/ace.jpg"


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def r_post_save_receiver(sender, instance, created, *args, **kwargs):
    use = user_.objects.get(id=instance.user_id)
    use.profiled = True
    use.save()


pre_save.connect(rl_pre_save_receiver, sender=Profile)
post_save.connect(r_post_save_receiver, sender=Profile)


class FollowBridge(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="m_follower"
    )
    followed = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="m_followed"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.email} and {self.followed.user.email}"
