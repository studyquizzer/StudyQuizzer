from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from crackerbox_.model_exports import BOOK_CATEGORY_CHOICES


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        password=None,
        is_active=True,
        is_admin=False,
        is_staff=False,
        is_profiled=False,
        is_resolver=True,
        is_reader=True,
        is_advanced=False,
        book_title=None,
        book_category=None,
    ):
        if not email:
            raise ValueError("User must enter an email address.")
        if not password:
            raise ValueError("User must enter a password.")
        if not username:
            raise ValueError("User must enter a username.")
        user_obj = self.model(
            email=self.normalize_email(email), username=username
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.profiled = is_profiled
        user_obj.is_resolver = is_resolver
        user_obj.is_reader = is_reader
        user_obj.is_advanced = is_advanced
        user_obj.book_title = book_title
        user_obj.book_category = book_category
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password, is_staff=True
        )
        return user

    def create_superuser(self, email, username, password=None, is_active=True):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )
        user.is_superuser = True
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profiled = models.BooleanField(default=False)
    username = models.CharField(
        unique=True, blank=True, null=True, max_length=20
    )
    is_reader = models.BooleanField(default=True)
    is_resolver = models.BooleanField(default=True)
    is_advanced = models.BooleanField(default=False)

    book_category = models.CharField(
        max_length=3, choices=BOOK_CATEGORY_CHOICES, blank=True, null=True
    )
    book_title = models.CharField(max_length=200, null=True, blank=True,)

    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        permissions = (
            ("read_only", "read_only_users"),
            ("resolver", "read, ask, comment, answer"),
            ("staff", "advanced users"),
        )
