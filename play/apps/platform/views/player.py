from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from apps.platform.forms import PlayerForm
from apps.platform.decorators import with_player


@login_required
@with_player
def edit(request):
    form = PlayerForm(instance=request.player)
    return render(request, "player/edit.html", {"form": form})


@login_required
@with_player
def update(request):
    form = PlayerForm(request.POST, instance=request.player)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Updated profile")
        return redirect("profile")
    return render(request, "player/edit.html", {"form": form})


@login_required
@with_player
def delete(request):
    user = request.user
    logout(request)
    request.player.delete()
    user.delete()
    return redirect("/")
