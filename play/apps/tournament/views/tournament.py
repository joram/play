from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentForm
from apps.tournament.models import TournamentGroup, Tournament, Heat
from apps.authentication.decorators import admin_required


@admin_required
@login_required
def index(request):
    user = request.user
    return render(request, 'tournament/list.html', {
        'tournament_groups': TournamentGroup.objects.all(),
        'tournaments': Tournament.objects.all(),
        'user': user,
    })


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save()
            messages.success(request, f'Tournament "{tournament.name}" successfully created')
            return redirect('/tournaments/')
    else:
        form = TournamentForm()

    return render(request, 'tournament/new.html', { 'form': form })


@admin_required
@login_required
def edit(request, id):
    tournament = Tournament.objects.get(id=id)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)

        if form.is_valid():
            form.save()
            messages.success(request, f'Tournament "{tournament.name}" updated')
            return redirect('/tournaments/')
    else:
        form = TournamentForm(instance=tournament)


    return render(request, 'tournament/edit.html', { 'form': form })


@admin_required
@login_required
def show(request, id):
    tournament = Tournament.objects.get(id=id)
    return render(request, 'tournament/show.html', { 'tournament': tournament })


@admin_required
@login_required
def create_game(request, id, heat_id):
    heat = Heat.objects.get(id=heat_id)
    heat.create_next_game()
    return redirect(f'/tournament/{id}/')

