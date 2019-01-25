from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from apps.tournament import urls as tournament_urls
from apps.authentication import urls as authentication_urls
from apps.snake import urls as snake_urls
from apps.game import urls as game_urls
from apps.leaderboard import urls as leaderboard_urls

urlpatterns = (
    authentication_urls.urlpatterns
    + game_urls.urlpatterns
    + tournament_urls.urlpatterns
    + snake_urls.urlpatterns
    + leaderboard_urls.urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
