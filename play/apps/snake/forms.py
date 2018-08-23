from django import forms
from django.forms import ValidationError
from apps.snake.models import Snake, UserSnake
from apps.utils.url import is_valid_url


class SnakeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label=f'Name',
        required=True,
        widget=forms.TextInput()
    )

    url = forms.CharField(
        max_length=100,
        label=f'URL',
        required=True,
        widget=forms.URLInput()
    )

    class Meta:
        model = Snake
        fields = ['name', 'url']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not is_valid_url(cleaned_data.get('url')):
            raise ValidationError('Snake requires a valid URL')

        return cleaned_data

    def save(self, *args, **kwargs):
        snake = super().save(*args, **kwargs)
        UserSnake.objects.get_or_create(
            user=self.user,
            snake=snake,
        )
        return snake
