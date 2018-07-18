from django import forms
from apps.game.engine import run_game


class GameForm(forms.Form):
    DEFAULT_HEIGHT = 20
    DEFAULT_WIDTH = 20
    DEFAULT_FOOD = 5
    MAX_SNAKES = 10

    width = forms.IntegerField(initial=DEFAULT_WIDTH)
    height = forms.IntegerField(initial=DEFAULT_HEIGHT)
    food = forms.IntegerField(initial=DEFAULT_FOOD)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, self.MAX_SNAKES + 1):
            self.fields[f'snake_name_{i}'] = forms.CharField(
                max_length=100,
                label=f'Snake {i} Name',
                required=False,
                widget=forms.TextInput()
            )

            self.fields[f'snake_url_{i}'] = forms.CharField(
                max_length=100,
                label=f'Snake {i} Url',
                required=False,
                widget=forms.URLInput()
            )

            # Note: This "groups" is used to create the form on the front end
            self.fields[f'snake_name_{i}'].group = 'snake'
            self.fields[f'snake_url_{i}'].group = 'snake'

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
        print(self.cleaned_data)
        return run_game(self.cleaned_data)
