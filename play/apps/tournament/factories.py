from apps.tournament.models import Team, TeamMember


class TeamFactory:
    def basic(self, user=None):
        team = Team.objects.create(name="test", description="test")
        if user:
            TeamMember.objects.create(team=team, user=user)
        return team
