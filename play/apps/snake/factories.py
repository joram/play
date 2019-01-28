from apps.snake.models import Snake, UserSnake


class SnakeFactory:
    def basic(self, n=1, commit=False, user=None):
        if n > 1:
            return [self.basic(commit=commit, user=user) for _ in range(n)]
        snake = Snake(name="test", url="http://foo.bar")
        if user:
            UserSnake.objects.create(user=user, snake=snake)
        if commit:
            snake.save()
        return snake
