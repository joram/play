from django import forms
from django.db.models import Q

from apps.core.models import Profile, Snake, Game, GameSnake


class ProfileForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    class Meta:
        model = Profile
        fields = ["optin_marketing"]
        labels = {
            "optin_marketing": "Opt in to occasional updates and marketing communication"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        profile.user.email = self.cleaned_data["email"]
        profile.user.save()
        return profile


class SnakeForm(forms.ModelForm):
    class Meta:
        model = Snake
        fields = ["name", "url", "is_public"]


class GameForm(forms.Form):
    """
        GameForm initializes a game and posts this to the engine to start the game.
        """

    board_size = forms.ChoiceField(
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
            ("custom", "Custom"),
        ],
        required=True,
        initial="medium",
    )
    width = forms.IntegerField(initial=11, required=False, disabled=True)
    height = forms.IntegerField(initial=11, required=False, disabled=True)
    snakes = forms.CharField(widget=forms.HiddenInput())

    def save(self, profile):
        data = self.cleaned_data
        game = Game.objects.create(
            width=data["width"], height=data["height"], max_turns_to_next_food_spawn=12
        )
        snake_ids = self.cleaned_data["snakes"].split(",")
        snakes = Snake.objects.filter(
            Q(id__in=snake_ids) & (Q(is_public=True) | Q(profile=profile))
        )
        for s in snakes.all():
            game.snakes.add(s)
        for snake_id in snake_ids:
            GameSnake.objects.create(snake=snakes.get(id=snake_id), game=game)
        game.save()
        return game
