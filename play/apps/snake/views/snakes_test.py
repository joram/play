from apps.authentication.factories import UserFactory
from apps.snake.factories import SnakeFactory
from apps.snake.models import UserSnake

user_factory = UserFactory()
snake_factory = SnakeFactory()


def test_index(client):
    user = user_factory.login_as(client)
    snake_factory.basic(n=8, commit=True, user=user)
    response = client.get('/snakes/')
    assert response.status_code == 200


def test_new(client):
    user_factory.login_as(client)
    response = client.get('/snakes/new/')
    assert response.status_code == 200


def test_create(client):
    user = user_factory.login_as(client)
    response = client.post('/snakes/', {
        'name': 'test2',
        'url': 'http://example.com',
    }, follow=True)
    assert response.status_code == 200
    assert UserSnake.objects.get(user=user).snake.name == 'test2'


def test_edit(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True, user=user)
    response = client.get(f'/snakes/{snake.id}/edit/')
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True, user=user)
    response = client.post(f'/snakes/{snake.id}/', {
        'name': 'testnew',
        'url': 'http://example.com',
        '_method': 'PUT',
    })
    assert response.status_code == 302
    snake.refresh_from_db()
    assert snake.name == 'testnew'


def test_delete(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True, user=user)
    response = client.delete(f'/snakes/{snake.id}/')
    assert response.status_code == 302
