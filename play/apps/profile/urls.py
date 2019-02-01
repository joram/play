from django.conf.urls import url
from apps.profile import views
from util.routing import method_dispatch

urlpatterns = [
    url(
        r"^profile/$",
        method_dispatch(GET=views.profile.view, POST=views.profile.view),
        name="profile",
    )
]
