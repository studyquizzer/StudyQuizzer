from django.contrib import admin

from user_profile.models import FollowBridge, Profile


# @admin.register(FollowBridge)
# class FollowBridgeAdmin(admin.ModelAdmin):
#     list_display = ("follower", "followed")
#     fields = ["follower", "followed"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "sex", "age", "slug")
    fields = [
        "user",
        "first_name",
        "last_name",
        "occupation",
        "sex",
        "age",
        "slug",
        "pic",
        "points",
        "website"
        # "follow",
    ]
    # inlines = [FollowerInline]
