from django import forms
from django.utils.translation import gettext as _
from apps.tournament.models import Team, TeamMember
from apps.authentication.models import User


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        team = super().save(*args, **kwargs)
        TeamMember.objects.create(
            user=self.user,
            team=team,
        )
        return team


class AddTeamMemberForm(forms.Form):
    username = forms.CharField()

    def __init__(self, user, team, *args, **kwargs):
        self.user = user
        self.team = team
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            cleaned_data['user'] = User.objects.get(
                username=cleaned_data['username'].lower()
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                _('User does not exist: %(username)s'),
                params={'username': cleaned_data['username']},
            )

        try:
            TeamMember.objects.get(
                user_id=cleaned_data['user'].id, team_id=self.team.id)
            raise forms.ValidationError(
                _('User already belongs to a team: %(username)s'),
                params={'username': cleaned_data['username']},
            )
        except TeamMember.DoesNotExist:
            pass

        return cleaned_data

    def save(self, *args, **kwargs):
        return TeamMember.objects.create(
            user=self.cleaned_data['user'],
            team=self.team,
        )
