from django.shortcuts import render
from apps.core.models import Profile, Snake


def show(request, username):
    profile = Profile.objects.get(user__username=username)
    snakes = Snake.objects.filter(profile=profile)
    return render(
        request, "profiles/show.html", {"profile": profile, "snakes": list(snakes)}
    )
