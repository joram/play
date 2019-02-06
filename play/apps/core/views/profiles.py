from django.shortcuts import render
from apps.core.models import Profile
from apps.core.middleware import profile_required


@profile_required
def show(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, "profiles/show.html", {"profile": profile})
