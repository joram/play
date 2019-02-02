from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.game.models import Game
from apps.utils.helpers import generate_game_url


def index(request):

    statuses = (
        Game.Status.PENDING,
        Game.Status.RUNNING,
        Game.Status.STOPPED,
        Game.Status.COMPLETE,
    )
    games = Game.objects.filter(status__in=statuses).order_by("-created")[:6]
    return render(
        request,
        "home.html",
        {
            "games": [
                {
                    "url": generate_game_url(g.engine_id)
                    + "&autoplay=true&hideScoreboard=true",
                    "engine_id": g.engine_id,
                }
                for g in games
            ]
        },
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")


def send_to_login(request):
    return redirect("/login")
