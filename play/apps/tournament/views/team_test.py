from apps.authentication.factories import UserFactory
from apps.snake.factories import SnakeFactory
from apps.tournament.factories import TeamFactory
from apps.tournament.models import TeamMember

user_factory = UserFactory()
team_factory = TeamFactory()
snake_factory = SnakeFactory()


def test_index(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True)
    team_factory.basic(user=user, snake=snake)
    response = client.get('/team/')
    assert response.status_code == 200


def test_index_redirect(client):
    user_factory.login_as(client)
    response = client.get('/team/')
    assert response.status_code == 302


def test_create(client):
    user = user_factory.login_as(client)
    response = client.post('/team/new/', {
        'name': 'test2',
        'description': 'test',
        'snake_url': 'http://example.com',
    })
    assert response.status_code == 302
    assert TeamMember.objects.get(user=user) is not None


def test_edit(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True)
    team_factory.basic(user=user, snake=snake)
    response = client.get(f'/team/edit/')
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(commit=True, user=user)
    team = team_factory.basic(user=user, snake=snake)
    response = client.post(f'/team/', {
        'name': 'test3',
        'description': 'test',
        'snake_url': 'http://example.com',
        '_method': 'put',
    })
    assert response.status_code == 302
    snake.refresh_from_db()
    team.refresh_from_db()
    assert snake.name == 'test3'
    assert snake.url == 'http://example.com'
    assert team.name == 'test3'
