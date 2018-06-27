from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.models import TeamMember
from apps.tournament.forms import TeamForm
from apps.tournament.middleware import with_current_team


@login_required
@with_current_team
def index(request):
    user = request.user
    team = request.team
    return render(request, 'team/show.html', {
        'team': team,
        'members': TeamMember.objects.filter(team_id=team.id),
        'user': user,
    })


@login_required
def new(request):
    return render(request, 'team/new.html', {
        'form': TeamForm(request.user),
    })


@login_required
@with_current_team
def edit(request):
    user = request.user
    team = request.team
    return render(request, 'team/edit.html', {
        'form': TeamForm(request.user, instance=team),
        'user': user,
    })


@login_required
@transaction.atomic
def create(request):
    form = TeamForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        return redirect('/team')
    return render(request, 'team/new.html', {
        'form': form,
    })


@login_required
@with_current_team
@transaction.atomic
def update(request):
    form = TeamForm(request.user, request.POST, instance=request.team)
    if form.is_valid():
        form.save()
        return redirect('/team')
    return render(request, 'team/edit.html', {
        'form': form,
    })
