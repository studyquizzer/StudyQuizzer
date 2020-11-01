from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_profile.models import Profile


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import *

User = get_user_model()
# admin.site.unregister(User)


class ProfileInline(admin.TabularInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "is_admin", "username")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username",)}),
        ("Book", {"fields": ("book_title", "book_category")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_active",
                    "profiled",
                    "is_reader",
                    "is_resolver",
                    "is_advanced",
                )
            },
        ),
        (
            "groups",
            {"classes": ("wide",), "fields": ("groups", "user_permissions",)},
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating auser.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()
    inlines = [ProfileInline]


admin.site.register(User, UserAdmin)

# @admin.register(User)
