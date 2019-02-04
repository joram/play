from django.shortcuts import render
from apps.platform.models import Player


def show(request, username):
    player = Player.objects.get(user__username=username)
    return render(request, "players/show.html", {"player": player})
