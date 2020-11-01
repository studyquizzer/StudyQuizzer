from django.conf import settings
from django.db import models


class Chat(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="first_user",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="second_user",
    )
    roomId = models.CharField(max_length=30, default="0")

    def __str__(self):
        return f"{self.user1} and {self.user2} in {self.roomId}"


class Chatkit(models.Model):
    tokenProvider = models.CharField(max_length=120, default="0")
    instanceLocator = models.CharField(max_length=100, default="0")

    def __str__(self):
        return f"{self.instanceLocator}--{self.tokenProvider}"
