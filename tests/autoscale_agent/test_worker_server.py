from autoscale_agent.worker_server import WorkerServer
from tests.helpers import TOKEN


def test_serve():
    server = WorkerServer(TOKEN, lambda: 1.23)
    assert server.serve() == 1.23
