from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament
from apps.snake.models import Snake


@login_required
def index(request):
    user = request.user
    # tournament = request.tournament
    return render(request, 'tournament/show.html', {
        # 'tournament': tournament,
        'user': user,
    })


@login_required
def edit(request):
    user = request.user
    t = Tournament()
    tournament = TournamentForm(tournament=t, instance=t)
    return render(request, 'tournament/edit.html', {
        'form': TournamentForm(request.user, instance=tournament),
        'user': user,
    })


@login_required
@transaction.atomic
def new(request):
    # Don't use the middleware here, check manually.
    # If the user is on a tournament already, don't let them make a new one.
    if request.user.assigned_to_tournament():
        messages.warning(request, "You're already assigned to a tournament")
        return redirect('/tournament')

    if request.method == 'POST':
        form = TournamentForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your tournament was created successfully')
            return redirect('/tournament')
        else:
            status = 400
    else:
        status = 200
        form = TournamentForm(request.user)

    return render(request, 'tournament/new.html', {
        'form': form,
    }, status=status)


@login_required
@transaction.atomic
def update(request):
    form = TournamentForm(request.user, request.POST, instance=request.tournament)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your tournament was updated successfully')
        return redirect('/tournament')

    return render(request, 'tournament/edit.html', {
        'form': form,
    }, status=400)
