from django.shortcuts import render
from apps.core.models import Profile


def show(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, "profiles/show.html", {"profile": profile})
