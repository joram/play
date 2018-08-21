import mock
from apps.authentication.factories import UserFactory

user_factory = UserFactory()


def test_new(client):
    user_factory.login_as(client)
    response = client.get('/games/new/')
    assert response.status_code == 200


def test_show(client):
    id = 'a879f127-55c2-4b0c-99c9-bce09c9fc0cf'
    user_factory.login_as(client)
    response = client.get(f'/games/{id}/')
    url = "game=a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
    assert response.status_code == 200
    assert url in response.content.decode('utf-8')


@mock.patch('apps.game.engine.run')
def test_create(mock_run, client):
    id = 'a879f127-55c2-4b0c-99c9-bce09c9fc0cf'
    mock_run.return_value = id
    user_factory.login_as(client)
    response = client.post(f'/games/new/', {
        'width': 10,
        'height': 10,
        'food': 10,
        # snake formset
        'snake-TOTAL_FORMS': 1,
        'snake-INITIAL_FORMS': 0,
        'snake-MIN_NUM_FORMS': 1,
        'snake-MAX_NUM_FORMS': 10,
        'snake-0-name': 'foo',
        'snake-0-url': 'http://example.com',
    })

    assert response.status_code == 302
    assert len(mock_run.call_args_list) == 1
