from apps.snake.models import Snake


class SnakeFactory:
    def basic(self, n=1, commit=False):
        if n > 1:
            return [self.basic(commit=commit) for _ in range(n)]
        snake = Snake(
            name='test',
            url='test',
        )
        if commit:
            snake.save()
        return snake
