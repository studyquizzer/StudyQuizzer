import notifications.urls
from crackerbox_.views import docjson
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from qa.views import base_home
from user_profile.views import update__profile
from users.views import signup

# from django.conf.urls import handler404


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_home, name="home"),
    path("cbox/", include("qa.urls")),
    path("martor/", include("martor.urls")),
    path("messages/", include("chat.urls",)),
    path("crackerbox/", include("crackerbox_.urls")),
    path("profile/", include("user_profile.urls")),
    path("signup/", signup, name="signup"),
    path("update/", update__profile.as_view(), name="update-profile"),
    path("docjson/crackerbox/documents/<uuid:id>", docjson, name="docjson"),
    path(
        "inbox/notifications/",
        include(notifications.urls, namespace="notifications"),
    ),
    # path('api/', include('rest.urls', )),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]
# handler404 = c_box.error_404
# handler500 = c_box.error_500
