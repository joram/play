from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from apps.core.forms import ProfileForm
from apps.core.middleware import with_profile


@login_required
@with_profile
def edit(request):
    form = ProfileForm(instance=request.user.profile)
    return render(request, "profile/edit.html", {"form": form})


@login_required
@with_profile
def update(request):
    form = ProfileForm(request.POST, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Updated profile")
        return redirect("profile")
    return render(request, "profile/edit.html", {"form": form}, status=400)


@login_required
@with_profile
def delete(request):
    user = request.user
    logout(request)
    user.delete()
    user.profile.delete()
    return redirect("/")
