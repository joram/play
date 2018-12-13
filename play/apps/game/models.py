from django.db import models, transaction
from util.fields import ShortUUIDField
from util.models import BaseModel
from apps.tournament.models import Team
from apps.game import engine
from apps.snake.models import Snake


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
        PENDING = 'pending'
        RUNNING = 'running'
        ERROR = 'error'
        STOPPED = 'stopped'
        COMPLETE = 'complete'

    id = ShortUUIDField(prefix='gam', max_length=128, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    engine_id = models.CharField(null=True, max_length=128)
    status = models.CharField(default=Status.PENDING, max_length=30)
    turn = models.IntegerField(default=0)
    width = models.IntegerField()
    height = models.IntegerField()
    food = models.IntegerField()
    is_leaderboard_game = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        self.snakes = kwargs.get('snakes', [])
        if 'snakes' in kwargs:
            del kwargs['snakes']
        super().__init__(*args, **kwargs)

    def config(self):
        """ Fetch the engine configuration. """
        config = {
            'width': self.width,
            'height': self.height,
            'food': self.food,
            'snakes': [],
        }
        for snake in self.get_snakes():
            config['snakes'].append({
                'name': snake.snake.name,
                'url': snake.snake.url,
                'id': snake.id,
            })
        return config

    def create(self):
        with transaction.atomic():
            # Note: Creating GameSnake
            # objects used to happen in the overridden save model function.
            # Saving the game here ensures there is an ID to use when
            # creating GameSnake objects. This is a bit of a hack because
            # of the way Game was implemented initially and then adapted to
            # support multiple of the same Snake in a Game.
            self.save()

            for s in self.snakes:
                snake = Snake.objects.get(id=s['id'])
                GameSnake.objects.create(snake=snake, game=self)

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
            self.status = status['status']
            self.turn = status['turn']

            for game_snake in self.get_snakes():
                snake_status = status['snakes'][game_snake.id]
                game_snake.death = snake_status['death']
                game_snake.save()

            self.save()
            return status

    def get_snakes(self):
        return GameSnake.objects.filter(game_id=self.id).prefetch_related('snake')

    def alive_game_snakes(self):
        return self.get_snakes().filter(death="pending")

    def winner(self):
        if self.status == self.Status.COMPLETE:
            living_snakes = self.alive_game_snakes()
            if len(living_snakes) == 1:
                return self.alive_game_snakes()[0]

    class Meta:
        app_label = 'game'


class GameSnake(BaseModel):
    id = ShortUUIDField(prefix='gs', max_length=128, primary_key=True)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    death = models.CharField(default='pending', max_length=128)
    turns = models.IntegerField(default=0)

    class Meta:
        app_label = 'game'
