from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("", include("apps.game.urls")),
    path("", include("apps.leaderboard.urls")),
    path("", include("apps.tournament.urls")),
    path("", include("apps.snake.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
