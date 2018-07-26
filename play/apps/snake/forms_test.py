from apps.snake.forms import SnakeForm
from apps.authentication.factories import UserFactory
from apps.snake.models import UserSnake


user_factory = UserFactory()


def test_create_form():
    user = user_factory.basic()
    user.save()

    form = SnakeForm(user, {
        'name': 'test',
        'url': 'test',
    })
    assert form.is_valid()

    snake = form.save()
    user_snake = UserSnake.objects.get(snake=snake)
    assert user_snake.user.id == user.id


def test_create_invalid_form():
    user = user_factory.basic()
    user.save()

    form = SnakeForm(user, {
        'name': '',
        'url': 'test',
    })
    assert not form.is_valid()
