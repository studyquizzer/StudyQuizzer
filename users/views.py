from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from users.forms import SignUpForm
from django_q.tasks import async_task



def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            authenticate(email=email, password=raw_password)
            user = form.save()

            login(
                request, user,
            )
            async_task('users.utils.sendemail', email, username)
            return redirect("make_profiled")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

