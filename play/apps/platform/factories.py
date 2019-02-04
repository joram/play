from apps.platform.models import Player, Snake


class PlayerFactory:
    def player(self, user):
        return Player.objects.create(user=user)


class SnakeFactory:
    def snake(self, player, n=1, commit=True):
        if n > 1:
            return [self.basic(player, commit=commit) for _ in range(n)]
        snake = Snake(name="test", url="http://foo.bar", player=player)
        if commit:
            snake.save()
        return snake
