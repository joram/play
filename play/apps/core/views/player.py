from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from apps.core.forms import ProfileForm


@login_required
def edit(request):
    form = ProfileForm(instance=request.user.profile)
    return render(request, "profile/edit.html", {"form": form})


@login_required
def update(request):
    form = ProfileForm(request.POST, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Updated profile")
        return redirect("profile")
    return render(request, "profile/edit.html", {"form": form}, status=400)


@login_required
def delete(request):
    user = request.user
    logout(request)
    request.user.profile.delete()
    user.delete()
    return redirect("/")
