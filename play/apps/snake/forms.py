from django import forms
from apps.snake.models import Snake, UserSnake


class SnakeForm(forms.ModelForm):
    class Meta:
        model = Snake
        fields = ['name', 'url']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        snake = super().save(*args, **kwargs)
        UserSnake.objects.get_or_create(
            user=self.user,
            snake=snake,
        )
        return snake
