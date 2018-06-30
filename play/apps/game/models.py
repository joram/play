from django.db import models, transaction
from util.fields import ShortUUIDField
from apps.game import engine
from apps.snake.models import Snake


class Game(models.Model):
    class Status:
        PENDING = 'pending'
        RUNNING = 'running'
        ERROR = 'error'
        STOPPED = 'stopped'
        COMPLETE = 'complete'

    id = ShortUUIDField(prefix='gam', max_length=128, primary_key=True)
    engine_id = models.CharField(null=True, max_length=128)
    status = models.CharField(default=Status.PENDING, max_length=30)
    turn = models.IntegerField(default=0)
    width = models.IntegerField()
    height = models.IntegerField()
    food = models.IntegerField()

    def __init__(self, *args, **kwargs):
        self.snakes = kwargs.get('snakes', [])
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # For all loaded snakes ensure that they exist.
            for s in self.snakes:
                GameSnake.objects.get_or_create(snake=s, game=self)
            return super().save(*args, **kwargs)

    def config(self):
        gsnakes = GameSnake.objects.filter(game_id=self.id).prefetch_related('snake')
        config = {
            'width': self.width,
            'height': self.height,
            'food': self.food,
            'snakes': [],
        }
        for snake in gsnakes:
            config['snakes'].append({
                'name': snake.snake.name,
                'url': snake.snake.url,
                'id': snake.snake.id,
            })
        return config

    def run(self):
        config = self.config()
        self.engine_id = engine.run(config)
        self.save()
        return self.engine_id

    def update_from_engine(self):
        with transaction.atomic():
            status = engine.status(self.engine_id)
            self.status = status['status']
            self.turn = status['turn']
            for game_snake in GameSnake.objects.filter(game_id=self.id)\
                                               .prefetch_related('snake'):
                snake_status = status['snakes'][game_snake.snake.id]
                game_snake.death = snake_status['death']
                game_snake.save()
            self.save()

    class Meta:
        app_label = 'game'


class GameSnake(models.Model):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    death = models.CharField(default="pending", max_length=128)

    class Meta:
        app_label = 'game'
