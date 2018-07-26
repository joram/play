from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.models import TeamMember
from apps.tournament.forms import AddTeamMemberForm
from apps.tournament.middleware import with_current_team


@login_required
@with_current_team
def index(request):
    return redirect('/members/new')


@login_required
@with_current_team
def new(request):
    return render(request, 'members/new.html', {
        'form': AddTeamMemberForm(request.user, request.team),
    })


@login_required
@with_current_team
@transaction.atomic
def create(request):
    form = AddTeamMemberForm(request.user, request.team, request.POST)
    if form.is_valid():
        form.save()
        return redirect('/team')
    return render(request, 'members/new.html', {
        'form': form,
    }, status=400)


@login_required
@transaction.atomic
def delete(request, id=None):
    team = TeamMember.objects.get(user_id=request.user.id).team
    try:
        TeamMember.objects.get(user_id=id, team_id=team.id).delete()
    except TeamMember.DoesNotExist:
        pass
    return redirect('/team')
