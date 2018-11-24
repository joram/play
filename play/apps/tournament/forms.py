from django import forms
from django.forms import ValidationError
from apps.tournament.models import Team, TeamMember, Tournament
from apps.authentication.models import User
from apps.snake.models import Snake
from apps.utils.url import is_valid_url


class TeamForm(forms.ModelForm):
    snake_url = forms.CharField(
        max_length=255,
        label='URL',
        help_text='Be sure to add a <strong>valid</strong> Snake URL here before \
                    the tournament starts, otherwise you may not be able to compete!',
        required=False,
        widget=forms.URLInput()
    )

    class Meta:
        model = Team
        fields = ['name', 'description']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.load_snake_data()

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('snake_url') and not is_valid_url(cleaned_data.get('snake_url')):
            raise ValidationError('Snake requires a valid URL')

        return cleaned_data

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
    username = forms.CharField(required=True)

    def __init__(self, user, team, *args, **kwargs):
        self.user = user
        self.team = team
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        try:
            cleaned_data['user'] = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(f"Hmm, {username} can't be found. Have they logged in yet?")

        try:
            # If this lookup raises an exception, then we can continue
            team_name = TeamMember.objects.get(
                user_id=cleaned_data['user'].id,
                team_id=self.team.id
            ).team.name
            raise ValidationError(f'{username} already belongs to {team_name}')
        except TeamMember.DoesNotExist:
            pass

        return cleaned_data

    def save(self, *args, **kwargs):
        return TeamMember.objects.create(
            user=self.cleaned_data['user'],
            team=self.team,
        )


class TournamentForm(forms.Form):
    name = forms.CharField(required=True)

    def save(self, *args, **kwargs):
        tournament = Tournament.objects.create(
            name=self.cleaned_data['name'],
        )
        return tournament
