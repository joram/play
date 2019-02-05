from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.forms import SnakeForm
from apps.core.middleware import with_profile
from apps.core.models import Snake


def index(request, snake_id):
    snake = Snake.objects.get(id=snake_id)
    return render(request, "snake/show.html", {"snake": snake})


@login_required
@with_profile
def create(request):
    form = SnakeForm()
    if request.POST:
        form = SnakeForm(request.POST)
        if form.is_valid():
            form.save(profile=request.user.profile)
            return redirect(f"/u/{request.user.username}")
    return render(request, "snake/edit.html", {"form": form})
