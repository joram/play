from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.models import TeamMember
from apps.tournament.forms import AddTeamMemberForm
from apps.tournament.middleware import with_current_team


@login_required
@with_current_team
def index(request):
    return redirect("/team/members/new")


@login_required
@with_current_team
@transaction.atomic
def new(request):
    if request.method == "POST":
        form = AddTeamMemberForm(request.user, request.team, request.POST)
        if form.is_valid():
            member = form.save()
            username = member.user.username
            messages.success(request, f"{username} successfully added to team")
            return redirect("/team")
        else:
            status = 400
    else:
        status = 200
        form = AddTeamMemberForm(request.user, request.team)

    return render(request, "members/new.html", {"form": form}, status=status)


@login_required
@transaction.atomic
def delete(request, id=None):
    team = TeamMember.objects.get(user_id=request.user.id).team
    try:
        member = TeamMember.objects.get(user_id=id, team_id=team.id)
        username = member.user.username
        member.delete()
        messages.success(request, f"{username} successfully removed from team")
    except TeamMember.DoesNotExist:
        pass
    return redirect("/team")
