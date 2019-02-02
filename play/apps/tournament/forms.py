from django import forms
from django.forms import ValidationError

from apps.authentication.models import User
from apps.snake.models import Snake
from apps.tournament.models import (
    Team,
    TeamMember,
    TournamentBracket,
    Tournament,
    TournamentSnake,
)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.load_snake_data()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def load_snake_data(self):
        if self.instance and self.instance.snake_id:
            self.snake = self.instance.snake
            self.initial["snake_url"] = self.instance.snake.url
        else:
            self.snake = Snake()

    def save(self, *args, **kwargs):
        self.snake.name = self.cleaned_data["name"]
        self.snake.save()

        team = super().save(commit=False)
        team.snake = self.snake
        team.save()

        TeamMember.objects.get_or_create(user=self.user, team=team)
        return team


class AddTeamMemberForm(forms.Form):
    username = forms.CharField(required=True)

    def __init__(self, user, team, *args, **kwargs):
        self.user = user
        self.team = team
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        try:
            cleaned_data["user"] = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(
                f"Hmm, {username} can't be found. Have they logged in yet?"
            )

        try:
            # If this lookup raises an exception, then we can continue
            team_name = TeamMember.objects.get(
                user_id=cleaned_data["user"].id, team_id=self.team.id
            ).team.name
            raise ValidationError(f"{username} already belongs to team {team_name}")
        except TeamMember.DoesNotExist:
            pass

        return cleaned_data

    def save(self, *args, **kwargs):
        return TeamMember.objects.create(user=self.cleaned_data["user"], team=self.team)


class TournamentBracketForm(forms.ModelForm):
    snakes = forms.ModelMultipleChoiceField(Snake.objects.all(), required=False)

    class Meta:
        model = TournamentBracket
        fields = ["name", "snakes", "board_width", "board_height", "board_food"]


class TournamentForm(forms.ModelForm):
    # snakes = forms.ModelMultipleChoiceField(Snake.objects.all(), required=False)

    class Meta:
        model = Tournament
        fields = ["name", "date", "status", "single_snake_per_team"]


class TournamentSnakeForm(forms.ModelForm):
    def __init__(self, user, tournament, snake, bracket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = TeamMember.objects.get(user=user).team
        self.user = user
        self.snake = snake
        self.tournament = tournament
        self.fields["snake"].choices = [(s.id, s.name) for s in self.team.snakes]
        self.initial["snake"] = snake
        self.fields["bracket"].choices = [
            (b.id, b.name) for b in self.tournament.brackets
        ]
        self.initial["bracket"] = bracket

    def is_valid(self):
        return self.tournament.status == Tournament.REGISTRATION

    def save(self, *args, **kwargs):
        if self.tournament.single_snake_per_team:
            qs = TournamentSnake.objects.filter(
                snake__in=self.team.snakes, tournament=self.tournament
            )
            qs.delete()

        ts, _ = TournamentSnake.objects.get_or_create(
            snake=self.snake, bracket=self.bracket, tournament=self.tournament
        )
        return ts

    class Meta:
        model = TournamentSnake
        fields = ["bracket", "snake"]
