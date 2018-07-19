from django import forms
from apps.game import engine


class GameForm(forms.Form):
    """
    GameForm initializes a game and posts this to the backend to start the game.
    this should be massively improved as the HTML is pretty ugly that it
    produces.
    """
    MAX_SNAKES = 10

    width = forms.IntegerField(initial=10)
    height = forms.IntegerField(initial=10)
    food = forms.IntegerField(initial=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(self.MAX_SNAKES):
            self.fields[f'snake_name_{i}'] = forms.CharField(
                max_length=100, label=f'Snake {i} Name',
                required=False,
            )
            self.fields[f'snake_url_{i}'] = forms.CharField(
                max_length=100, label=f'Snake {i} Url',
                required=False,
            )

    def clean(self):
        cleaned_data = super().clean()
        snakes = []
        for key in cleaned_data.keys():
            if key.startswith('snake_name_') and cleaned_data[key]:
                idx = int(key.split('_')[-1])
                snakes.append({
                    'name': self.cleaned_data[key],
                    'url': self.cleaned_data[f'snake_url_{idx}']
                })
        return {
            'width': cleaned_data['width'],
            'height': cleaned_data['height'],
            'food': cleaned_data['food'],
            'snakes': snakes,
        }

    def submit(self):
        return engine.run(self.cleaned_data)
