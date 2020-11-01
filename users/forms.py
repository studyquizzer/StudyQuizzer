from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(UserAdminChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ("username", "email", "password", "is_active", "is_admin")

    def save(self, *args, **kwargs):
        user = super(UserAdminChangeForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        return user


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required", widget=forms.TextInput()
    )
    username = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        # Add the things your super doesn't do for you
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )
