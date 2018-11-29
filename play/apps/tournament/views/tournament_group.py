from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentGroupForm
from apps.tournament.models import TournamentGroup
from apps.authentication.decorators import admin_required


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        form = TournamentGroupForm(request.POST)

        if form.is_valid():
            tournament_group = form.save()
            messages.success(request, 'Tournament group successfully created')
            return redirect('/tournaments/')

    else:
        form = TournamentGroupForm()

    return render(request, 'tournament_group/new.html', { 'form': form })

@admin_required
@login_required
def edit(request, id):
    tournament_group = TournamentGroup.objects.get(id=id)

    if request.method == 'POST':
        form = TournamentGroupForm(request.POST, instance=tournament_group)

        if form.is_valid():
            form.save()
            messages.success(request, f'Tournament group "{tournament_group.name}" updated')
            return redirect('/tournaments/')
    else:
        form = TournamentGroupForm(instance=tournament_group)

    return render(request, 'tournament_group/edit.html', { 'form': form })
