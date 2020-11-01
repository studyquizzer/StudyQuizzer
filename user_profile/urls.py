from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProfileAdds.as_view(), name="make_profiled"),
]
