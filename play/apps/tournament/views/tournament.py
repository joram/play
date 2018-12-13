from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament, TournamentBracket
from apps.authentication.decorators import admin_required


@admin_required
@login_required
def index(request):
    user = request.user
    return render(request, 'tournament/list.html', {
        'tournaments': Tournament.objects.all(),
        'tournament_brackets': TournamentBracket.objects.all(),
        'user': user,
    })


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament_group = form.save()
            messages.success(request, 'Tournament group successfully created')
            return redirect('/tournaments/')

    else:
        form = TournamentForm()

    return render(request, 'tournament/new.html', { 'form': form })


@admin_required
@login_required
def edit(request, id):
    tournament_group = Tournament.objects.get(id=id)

    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament_group)

        if form.is_valid():
            form.save()
            messages.success(request, f'Tournament group "{tournament_group.name}" updated')
            return redirect('/tournaments/')
    else:
        form = TournamentForm(instance=tournament_group)

    return render(request, 'tournament/edit.html', { 'form': form })
