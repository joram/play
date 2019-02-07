from django.db import models, transaction

from apps.core.models import Snake
from apps.game import engine
from util.fields import ShortUUIDField
from util.models import BaseModel


class Game(BaseModel):
    """
        Game tracks a game started on the engine locally in the snake database. You
        can initialize a game through this model and call run() to start the game.
        Then, you can also call update_from_engine() at any point to refresh the
        game state from the engine onto this model.

        Creating a game looks like:

            game = Game(...) # instance created with config, ready to go
            game.create()    # game snakes created, and any other future pre-game things
            game.run()       # sent to engine, and now it's running!
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
    max_turns_to_next_food_spawn = models.IntegerField(default=15)
    snakes = models.ManyToManyField(Snake)

    def config(self):
        """ Fetch the engine configuration. """
        config = {
            "width": self.width,
            "height": self.height,
            "maxTurnsToNextFoodSpawn": self.max_turns_to_next_food_spawn,
            "food": self.snakes.count(),
            "snakes": [
                {"name": snake.name, "url": snake.url, "id": snake.id}
                for snake in self.snakes.all()
            ],
        }
        return config

    def create(self):
        config = self.config()
        self.engine_id = engine.create(config)
        self.save()

    def run(self):
        """ Call the engine to start the game. Returns the game id. """
        engine.run(self.engine_id)
        return self.engine_id

    def update_from_engine(self):
        """ Update the status and snake statuses from the engine. """
        with transaction.atomic():
            status = engine.status(self.engine_id)
            self.status = status["status"]
            self.turn = status["turn"]

            # for game_snake in self.get_snakes():
            #     snake_status = status["snakes"][game_snake.id]
            #     game_snake.death = snake_status["death"]
            #     game_snake.save()

            self.save()
            return status
