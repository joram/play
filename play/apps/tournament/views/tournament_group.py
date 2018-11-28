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
    return render(request, 'tournament_group/new.html', {
        'form': TournamentGroupForm(),
    })


@admin_required
@login_required
@transaction.atomic
def create(request):
    form = TournamentGroupForm(request.POST)
    if form.is_valid():
        tournament_group = form.save()
        messages.success(request, 'Tournament successfully created')
        return redirect('/tournament_group/%d/edit/' % tournament_group.id)
    return render(request, 'tournament_group/new.html', {
        'form': form,
    }, status=400)


@admin_required
@login_required
def edit(request, id):
    tg = TournamentGroup.objects.get(id=id)
    form = TournamentGroupForm()
    form.name = tg.name
    form.date = tg.date
    if form.is_valid():
        tg.name = form.name
        tg.date = form.date
        tg.save()
    return render(request, 'tournament_group/edit.html', {
        'form': form,
        'tournament_group': tg,
    })
