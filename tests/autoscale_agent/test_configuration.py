import pytest
from unittest.mock import MagicMock
from autoscale_agent.configuration import Configuration, InvalidPlatformError
from autoscale_agent.web_dispatcher import WebDispatcher
from autoscale_agent.worker_dispatcher import WorkerDispatcher
from autoscale_agent.worker_server import WorkerServer
from tests.helpers import PLATFORM, TOKEN


def test_run_calls():
    config = Configuration(PLATFORM)
    mock_web_dispatchers_run = MagicMock()
    mock_worker_dispatchers_run = MagicMock()
    config.web_dispatchers.run = mock_web_dispatchers_run
    config.worker_dispatchers.run = mock_worker_dispatchers_run
    config.run()
    config.run()
    mock_web_dispatchers_run.assert_called_once()
    mock_worker_dispatchers_run.assert_called_once()


def test_platform():
    for p in [PLATFORM]:
        config = Configuration(p)
        assert config.platform == p


def test_platform_invalid():
    with pytest.raises(InvalidPlatformError):
        Configuration("whoami")


def test_dispatch_web():
    config = Configuration(PLATFORM).dispatch(TOKEN)
    assert isinstance(config.web_dispatchers.queue_time, WebDispatcher)


def test_dispatch_worker():
    config = Configuration(PLATFORM).dispatch(TOKEN, lambda: 1.23)
    assert isinstance(config.worker_dispatchers._dispatchers[0], WorkerDispatcher)
    assert len(config.worker_dispatchers._dispatchers) == 1


def test_serve_worker():
    config = Configuration(PLATFORM).serve(TOKEN, lambda: 1.23)
    assert isinstance(config.worker_servers._servers[0], WorkerServer)
    assert len(config.worker_servers._servers) == 1
