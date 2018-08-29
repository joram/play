import mock
import uuid
from apps.game.forms import GameForm


@mock.patch('apps.game.engine.run')
def test_submit(mock_run):
    engine_id = str(uuid.uuid4())
    mock_run.return_value = engine_id

    form = GameForm({
        'width': 10,
        'height': 10,
        'food': 10,
    }, snakes=[{'name': 'foo', 'url': 'http://example.com'}])

    assert form.is_valid()
    assert form.submit() == engine_id
    assert len(mock_run.call_args_list) == 1
