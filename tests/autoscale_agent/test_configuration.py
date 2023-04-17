import pytest
from autoscale_agent.configuration import Configuration, InvalidPlatformError
from autoscale_agent.web_dispatcher import WebDispatcher
from autoscale_agent.worker_dispatcher import WorkerDispatcher
from autoscale_agent.worker_server import WorkerServer
from tests.helpers import PLATFORM, TOKEN


def test_platform():
    for p in ["render"]:
        config = Configuration(p, run=False)
        assert config.platform == p

def test_platform_invalid():
    with pytest.raises(InvalidPlatformError):
        Configuration("whoami")

def test_dispatch_web():
    config = Configuration(PLATFORM, run=False).dispatch(TOKEN)
    dispatcher = config.web_dispatchers.queue_time
    assert isinstance(dispatcher, WebDispatcher)
    assert len(config.web_dispatchers) == 1

def test_dispatch_worker():
    config = Configuration(PLATFORM, run=False).dispatch(TOKEN, lambda: 1.23)
    dispatcher = config.worker_dispatchers[0]
    assert isinstance(dispatcher, WorkerDispatcher)
    assert len(config.worker_dispatchers) == 1

def test_serve_worker():
    config = Configuration(PLATFORM, run=False).serve(TOKEN, lambda: 1.23)
    server = config.worker_servers[0]
    assert isinstance(server, WorkerServer)
    assert len(config.worker_servers) == 1
