import re

from django import forms
from django.forms import ValidationError

from apps.game.models import Game
from apps.utils.url import is_valid_url

SNAKE_FORMSET_INDEX_REGEX = re.compile(r"^snake\-(\d+)")


def get_snakes_from_request(request_data):
    """
    `request_data` contains formset form data in a structure like
    ```
    {
        ...
        'snake-0-id: ...,
        'snake-0-name: ...,
        'snake-0-url: ...,
        'snake-1-id: ...,
        'snake-1-name: ...,
        'snake-1-url: ...,
        ...
    }
    ```
    but also contains other `request.POST` data so we only focus
    on keys that we're interested.
    """
    snakes = []
    for k, v in request_data.items():
        index = re.findall(SNAKE_FORMSET_INDEX_REGEX, k)
        if index:
            i = int(index[0])
            try:
                snakes[i]
            except IndexError:
                # The object at the current index doesn't exist
                # in the list yet, so add one
                snakes.append({})
            # Get snake data from the formset data in the request
            if "id" in k and v:
                snakes[i]["id"] = request_data.get(f"snake-{i}-id")
            if "name" in k and v:
                snakes[i]["name"] = request_data.get(f"snake-{i}-name")
            if "url" in k and v:
                snakes[i]["url"] = request_data.get(f"snake-{i}-url")

    # Filter out the empty snakes
    return [snake for snake in snakes if snake]


class SnakeForm(forms.Form):
    """
    SnakeForm initializes a row containing snake name and url
    """

    id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(widget=forms.HiddenInput())
    url = forms.CharField(widget=forms.HiddenInput())


class GameForm(forms.Form):
    """
    GameForm initializes a game and posts this to the engine to start the game.
    """

    board_sizes = forms.ChoiceField(
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
            ("custom", "Custom"),
        ],
        required=True,
    )
    width = forms.IntegerField(initial=20, required=False)
    height = forms.IntegerField(initial=20, required=False)
    food = forms.IntegerField(initial=5, required=True)

    def __init__(self, *args, **kwargs):
        self.snakes = kwargs.pop("snakes", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.snakes:
            raise ValidationError("Must add at least 1 snake to start a game")

        for snake in self.snakes:
            if not snake.get("name"):
                raise ValidationError("Snake requires a name")

            if not snake.get("url"):
                raise ValidationError("Snake requires a URL")

            if not is_valid_url(snake["url"]):
                raise ValidationError("Snake requires a valid URL")

        board_size = self.cleaned_data["board_sizes"]
        if board_size != "custom":
            if board_size == "large":
                self.cleaned_data["width"] = 19
                self.cleaned_data["height"] = 19
            elif board_size == "medium":
                self.cleaned_data["width"] = 11
                self.cleaned_data["height"] = 11
            elif board_size == "small":
                self.cleaned_data["width"] = 7
                self.cleaned_data["height"] = 7

        return {
            "width": self.cleaned_data["width"],
            "height": self.cleaned_data["height"],
            "food": self.cleaned_data["food"],
            "snakes": self.snakes,
        }

    def submit(self):
        game = Game(**self.cleaned_data)
        game.create()
        return game.run()
