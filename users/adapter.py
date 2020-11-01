# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from django.conf import settings
# from django.shortcuts import resolve_url
# from .models import User
# from user_profile.models import Profile
# from annoying.functions import get_object_or_None
#
# class AccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#         profile = get_object_or_None(Profile, user__email = request.user)#d.has_usable_password()
#         user_ = get_object_or_None(User, email=request.user )
#
#         if user_.has_usable_password():
#             if profile:
#                 url = settings.LOGIN_REDIRECT_URL
#             else:
#                 url = 'make_profiled'
#         # elif request.user.password == '!':
#         #     url = '/accounts/password/set/'
#         else:
#             url = settings.LOGIN_REDIRECT_URL
#         return resolve_url(url)
#
# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def get_connect_redirect_url(self, request, socialaccount):
#         profile = get_object_or_None(Profile, user__email = request.user)#d.has_usable_password()
#         user_ = get_object_or_None(User, email=request.user )
#
#         #assert request.user.is_authenticated()
#         if user_.has_usable_password():
#             if profile:
#                 url = settings.LOGIN_REDIRECT_URL
#             else:
#                 url = 'make_profiled'
#         # elif request.user.password == '!':
#         #     url = '/accounts/password/set/'
#         else:
#             url = '/accounts/password/set/'
#         return resolve_url(url)
