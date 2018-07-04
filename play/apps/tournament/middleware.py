from django.shortcuts import redirect
from apps.tournament.models import TeamMember


def with_current_team(action):
    def decorate(request, *args, **kwargs):
        user = request.user
        try:
            team = TeamMember.objects.get(user_id=user.id).team
            request.team = team
            return action(request, *args, **kwargs)
        except TeamMember.DoesNotExist:
            return redirect('/team/new')
    return decorate
