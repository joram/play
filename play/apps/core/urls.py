from django.conf.urls import url
from apps.core.views import profile, profiles
from util.routing import method_dispatch as route

urlpatterns = [
    url(
        r"^profile/$",
        route(GET=profile.edit, PUT=profile.update, DELETE=profile.delete),
        name="profile",
    ),
    url(r"^u/(?P<username>[\w\-]+)/$", route(GET=profiles.show), name="u"),
]
