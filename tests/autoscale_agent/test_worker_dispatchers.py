import pytest
from autoscale_agent.worker_dispatchers import WorkerDispatchers
from autoscale_agent.worker_dispatcher import WorkerDispatcher
from tests.helpers import TOKEN


def test_dispatch(mocker):
    dispatchers = WorkerDispatchers()
    dispatcher = WorkerDispatcher(TOKEN, lambda: None)
    dispatchers.append(dispatcher)
    mocker.patch.object(dispatcher, "dispatch")
    dispatchers.dispatch()
    for dispatcher in dispatchers._dispatchers:
        assert dispatcher.dispatch.called


def test_dispatch_exception(mocker, capsys):
    dispatchers = WorkerDispatchers()
    dispatcher = WorkerDispatcher(TOKEN, lambda: None)
    dispatchers.append(dispatcher)
    mocker.patch.object(dispatcher, "dispatch", side_effect=RuntimeError)
    dispatchers.dispatch()
    out, _ = capsys.readouterr()
    assert "Autoscale: RuntimeError" in out
