from django.db import models, transaction
from util.fields import ShortUUIDField
from util.models import BaseModel
from apps.game import engine
from apps.snake.models import Snake


class Game(BaseModel):
    """
    Game tracks a game started on the engine locally in the snake database. You
    can initialize a game through this model and call run() to start the game.
    Then, you can also call update_from_engine() at any point to refresh the
    game state from the engine onto this model.
    """

    class Status:
        PENDING = "pending"
        RUNNING = "running"
        ERROR = "error"
        STOPPED = "stopped"
        COMPLETE = "complete"

    id = ShortUUIDField(prefix="gam", max_length=128, primary_key=True)
    engine_id = models.CharField(null=True, max_length=128)
    status = models.CharField(default=Status.PENDING, max_length=30)
    turn = models.IntegerField(default=0)
    width = models.IntegerField()
    height = models.IntegerField()
    food = models.IntegerField()

    def __init__(self, *args, **kwargs):
        self.snakes = kwargs.get("snakes", [])
        if "snakes" in kwargs:
            del kwargs["snakes"]
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # For all loaded snakes ensure that they exist.
            for s in self.snakes:
                snake = Snake.objects.get(id=s['id'])
                GameSnake.objects.create(snake=snake, game=self)
            return super().save(*args, **kwargs)

    def config(self):
        """ Fetch the engine configuration. """
        gsnakes = GameSnake.objects.filter(game_id=self.id).prefetch_related("snake")
        config = {
            "width": self.width,
            "height": self.height,
            "food": self.food,
            "snakes": [],
        }
        for snake in gsnakes:
            config["snakes"].append(
                {"name": snake.snake.name, "url": snake.snake.url, "id": snake.snake.id}
            )
        return config

    def run(self):
        """ Call the engine to start the game. Returns the game id. """
        config = self.config()
        self.engine_id = engine.run(config)
        self.save()
        return self.engine_id

    def update_from_engine(self):
        """ Update the status and snake statuses from the engine. """
        with transaction.atomic():
            status = engine.status(self.engine_id)
            self.status = status["status"]
            self.turn = status["turn"]
            for game_snake in GameSnake.objects.filter(
                game_id=self.id
            ).prefetch_related("snake"):
                snake_status = status["snakes"][game_snake.snake.id]
                game_snake.death = snake_status["death"]
                game_snake.turns = snake_status["turn"]
                game_snake.save()
            self.save()

    def get_snakes(self):
        return GameSnake.objects.filter(game_id=self.id).prefetch_related('snake')

    class Meta:
        app_label = "game"


class GameSnake(models.Model):
    id = ShortUUIDField(prefix='gs', max_length=128, primary_key=True)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    death = models.CharField(default='pending', max_length=128)
    turns = models.IntegerField(default=0)

    class Meta:
        app_label = "game"
        unique_together = (("snake", "game"),)
