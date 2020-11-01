from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import (
    CreateView,
    FormView,
)

from users.models import User
from . import forms
from . import models


class ProfileAdds(LoginRequiredMixin, CreateView):
    form_class = forms.ProfileAdd
    template_name = "profile.html"
    message = "Thank you! your profile has been created."

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(ProfileAdds, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        user = self.request.user
        if user.is_authenticated:
            pass
        else:
            return redirect("login")
        profile = models.get_object_or_None(models.Profile, user=user)
        if profile:
            return redirect("update-profile")
        else:
            return super(ProfileAdds, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return models.reverse("home")


class update__profile(LoginRequiredMixin, FormView):
    form_class = forms.ProfileUpdate
    message = "Thank you! your profile has been updated."
    template_name = "profile_update.html"
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        try:
            profile = models.Profile.objects.get(user=self.request.user)
            return form_class(instance=profile, **self.get_form_kwargs())
        except profile.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context["form"] = form
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)

    def get_initial(self):
        profile_instance = get_object_or_404(
            models.Profile, user=self.request.user
        )
        return {
            "first_name": profile_instance.first_name,
            "last_name": profile_instance.last_name,
            "age": profile_instance.age,
            "sex": profile_instance.sex,
        }

    def get_success_url(self, **kwargs):
        profile_instance = get_object_or_404(
            models.Profile, user=self.request.user
        )
        return reverse_lazy(
            "user-profile", kwargs={"slug": profile_instance.slug}
        )


class UserDetailView(LoginRequiredMixin, generic.DetailView):  # to be revised.
    model = models.Profile
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(models.Profile, slug=slug)
        context["follower"] = models.FollowBridge.objects.filter(
            followed__user__email=obj.user.email
        )
        context["myself"] = obj
        context["following"] = models.FollowBridge.objects.filter(
            follower__user__email=obj.user.email
        )
        return context


class ToggleFollower(
    LoginRequiredMixin, generic.RedirectView
):  # to be revised.
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(models.Profile, slug=slug)
        user = self.request.user
        us = get_object_or_404(models.Profile, user__email=user)
        follower_ = list(
            models.FollowBridge.objects.filter(
                followed__user__email=obj.user.email
            ).values("follower__user__email")
        )
        if user.is_authenticated:
            if follower_:
                x = []
                for foll in follower_:
                    x.append(foll["follower__user__email"])
                if user.email in x:
                    pass
                else:
                    FollowBridgeobj = models.FollowBridge(
                        follower=us, followed=obj
                    )
                    FollowBridgeobj.save()
            else:
                FollowBridgeobj = models.FollowBridge(
                    follower=us, followed=obj
                )
                FollowBridgeobj.save()
        return obj.get_absolute_url()


class FollowerList(generic.ListView):  # to be revised.
    model = models.FollowBridge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        objs = get_object_or_404(models.Profile, slug=slug)
        context["follower_"] = models.FollowBridge.objects.filter(
            followed=objs
        )
        context["followed_"] = objs
        return context

    template_name = "followerlist.html"
    paginate_by = 4


class FollowingList(generic.ListView):  # to be revised.
    model = models.FollowBridge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        # slug = self.kwargs.get('slug')
        objs = get_object_or_404(models.Profile, slug=slug)
        context["followed_"] = models.FollowBridge.objects.filter(
            follower=objs
        )
        context["follower_"] = objs
        return context

    template_name = "followinglist.html"
    paginate_by = 4
