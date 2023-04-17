import pytest
from freezegun import freeze_time
from autoscale_agent.web_dispatchers import WebDispatchers, AlreadySetError
from autoscale_agent.web_dispatcher import WebDispatcher
from tests.helpers import TOKEN


def test_already_set_error():
    dispatchers = WebDispatchers()
    dispatchers.set_queue_time(WebDispatcher(TOKEN))
    with pytest.raises(AlreadySetError):
        dispatchers.set_queue_time(WebDispatcher(TOKEN))

def test_dispatch(mocker):
    dispatchers = WebDispatchers()
    dispatchers.set_queue_time(WebDispatcher(TOKEN))
    mocker.patch.object(dispatchers.queue_time, 'dispatch')
    dispatchers.dispatch()
    dispatchers.queue_time.dispatch.assert_called_once()

def test_dispatch_exception(mocker, capsys):
    dispatchers = WebDispatchers()
    dispatchers.queue_time = WebDispatcher(TOKEN)
    mocker.patch.object(dispatchers.queue_time, 'dispatch', side_effect=RuntimeError)
    dispatchers.dispatch()
    out, _ = capsys.readouterr()
    assert "Autoscale::Agent/WebDispatcher: RuntimeError" in out
