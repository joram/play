from apps.tournament.models import Team, TeamMember


class TeamFactory:
    def basic(self, snake=None, user=None):
        team = Team.objects.create(name="test", description="test", snake=snake)
        if user:
            TeamMember.objects.create(team=team, user=user)
        return team
