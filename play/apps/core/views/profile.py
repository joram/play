from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from apps.core.models import Profile
from apps.core.forms import ProfileForm
from apps.core.middleware import profile_required


@login_required
def edit(request):
    profile = Profile.objects.get_or_init(user=request.user)
    form = ProfileForm(instance=profile)
    return render(request, "profile/edit.html", {"form": form, "profile": profile})


@login_required
def update(request):
    profile = Profile.objects.get_or_init(user=request.user)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Updated profile")
        return redirect("profile")
    return render(
        request, "profile/edit.html", {"form": form, "profile": profile}, status=400
    )


@login_required
@profile_required
def delete(request):
    user = request.user
    logout(request)
    user.delete()
    if hasattr(user, "profile"):
        user.profile.delete()
    return redirect("/")
