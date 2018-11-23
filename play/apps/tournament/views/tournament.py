from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament, Heat
from apps.authentication.decorators import admin_required

@admin_required
@login_required
def index(request):
    user = request.user
    return render(request, 'tournament/list.html', {
        'tournaments': Tournament.objects.all(),
        'user': user,
    })


@admin_required
@login_required
@transaction.atomic
def new(request):
    return render(request, 'tournament/new.html', {
        'form': TournamentForm(),
    })


@admin_required
@login_required
@transaction.atomic
def create(request):
    form = TournamentForm(request.POST)
    if form.is_valid():
        tournament = form.save()
        messages.success(request, 'Tournament successfully created')
        return redirect('/tournament/%d/edit/' % tournament.id)
    return render(request, 'tournament/new.html', {
        'form': form,
    }, status=400)


@admin_required
@login_required
def edit(request, id):
    t = Tournament.objects.get(id=id)
    form = TournamentForm()
    form.name = t.name
    if form.is_valid():
        t.name = form.name
        t.save()
    return render(request, 'tournament/edit.html', {
        'form': form,
        'tournament': t,
    })


@admin_required
@login_required
def show(request, id):
    t = Tournament.objects.get(id=id)
    return render(request, 'tournament/show.html', {
        'tournament': t,
    })


@admin_required
@login_required
def create_game(request, id, heat_id):
    heat = Heat.objects.get(id=heat_id)
    heat.create_next_game()
    return redirect('/tournament/%s/' % id)

