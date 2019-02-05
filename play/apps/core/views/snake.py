from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.forms import SnakeForm
from apps.core.middleware import with_profile


def index(request):
    return render("snakes/show.html")


@login_required
@with_profile
def create(request):
    if request.POST:
        form = SnakeForm(request.POST)
        if form.is_valid():
            snake = form.save()
            return redirect(f"/s/{snake.id}")
    return render("snakes/edit.html")
