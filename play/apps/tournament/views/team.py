from django.shortcuts import render, redirect
from django.contrib import messages
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
    return render(
        request,
        "team/show.html",
        {
            "team": team,
            "members": TeamMember.objects.filter(team_id=team.id),
            "user": user,
        },
    )


@login_required
@with_current_team
def edit(request):
    user = request.user
    team = request.team
    return render(
        request,
        "team/edit.html",
        {"form": TeamForm(request.user, instance=team), "user": user},
    )


@login_required
@transaction.atomic
def new(request):
    # Don't use the middleware here, check manually.
    # If the user is on a team already, don't let them make a new one.
    if request.user.assigned_to_team():
        messages.warning(request, "You're already assigned to a team")
        return redirect("/team")

    if request.method == "POST":
        form = TeamForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your team was created successfully")
            return redirect("/team")
        else:
            status = 400
    else:
        status = 200
        form = TeamForm(request.user)

    return render(request, "team/new.html", {"form": form}, status=status)


@login_required
@with_current_team
@transaction.atomic
def update(request):
    form = TeamForm(request.user, request.POST, instance=request.team)
    if form.is_valid():
        form.save()
        messages.success(request, "Your team was updated successfully")
        return redirect("/team")

    return render(request, "team/edit.html", {"form": form}, status=400)
