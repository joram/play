from django.conf import settings


def window_globals(request):
    return {"ENGINE_URL": settings.ENGINE_URL}
