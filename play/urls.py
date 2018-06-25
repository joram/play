from django.conf.urls.static import static
from django.conf import settings

from apps.tournament import urls as tournament_urls
from apps.authentication import urls as authentication_urls

urlpatterns = authentication_urls.urlpatterns + \
    tournament_urls.urlpatterns + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
