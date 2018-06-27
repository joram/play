from django import forms
from django.utils.translation import gettext as _
from apps.tournament.models import Team, TeamMember
from apps.authentication.models import User
from apps.snake.models import Snake


class TeamForm(forms.ModelForm):
    snake_url = forms.CharField(max_length=255)

    class Meta:
        model = Team
        fields = ['name', 'description']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.load_snake_data()

    def load_snake_data(self):
        if self.instance and self.instance.snake_id:
            self.snake = self.instance.snake
            self.initial['snake_url'] = self.instance.snake.url
        else:
            self.snake = Snake()

    def save(self, *args, **kwargs):
        self.snake.url = self.cleaned_data['snake_url']
        self.snake.name = self.cleaned_data['name']
        self.snake.save()

        team = super().save(commit=False)
        team.snake = self.snake
        team.save()

        TeamMember.objects.get_or_create(
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
                username=cleaned_data['username']
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
