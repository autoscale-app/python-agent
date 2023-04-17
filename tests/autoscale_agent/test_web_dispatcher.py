import pytest
import json
import httpretty
from unittest.mock import patch
from freezegun import freeze_time
from tests.helpers import travel, TOKEN
from autoscale_agent.web_dispatcher import WebDispatcher


def test_id():
    dispatcher = WebDispatcher(TOKEN)
    assert "u4quBFg" == dispatcher.id

@httpretty.activate
def test_dispatch():
    httpretty.register_uri(
        httpretty.POST, "https://metrics.autoscale.app/",
        status=200, body="", headers={},
        match_requests_on=["method", "body", "headers"]
    )

    dispatcher = WebDispatcher(TOKEN)
    metrics = [[1], [0, 2, 1], [2, 1, 3], [1, 4, 3], [5, 4, 1], [6, 2, 6], [0, 3, 7]]
    for i in range(len(metrics)):
        with freeze_time(f"2000-01-01 00:00:{i+1}"):
            for metric in metrics[i]:
                dispatcher.add(metric)

    with freeze_time("2000-01-01 00:00:07"):
        dispatcher.dispatch()

    request = httpretty.last_request()

    assert request.headers.get("Content-Type") == "application/json"
    assert request.headers.get("User-Agent") == "Autoscale Agent (Python)"
    assert request.headers.get("Autoscale-Metric-Token") == TOKEN

    expected_body = {
        "946684801": 1,
        "946684802": 2,
        "946684803": 3,
        "946684804": 4,
        "946684805": 5,
        "946684806": 6
    }

    actual_body = json.loads(request.body.decode('utf-8'))
    assert actual_body == expected_body

@patch("autoscale_agent.request.dispatch")
def test_dispatch_empty(mock_dispatch):
    dispatcher = WebDispatcher(TOKEN)
    dispatcher.dispatch()
    mock_dispatch.assert_not_called()

@httpretty.activate
def test_dispatch_500(capsys):
    dispatcher = WebDispatcher(TOKEN)
    metrics = [[1], [0, 2, 1], [2, 1, 3], [1, 4, 3], [5, 4, 1], [6, 2, 6], [0, 3, 7]]

    for i in range(len(metrics)):
        with travel(i+1):
            for metric in metrics[i]:
                dispatcher.add(metric)

    httpretty.register_uri(
        httpretty.POST, "https://metrics.autoscale.app/",
        status=500, body="", headers={},
        match_requests_on=["method", "body", "headers"]
    )

    buffer = dispatcher.buffer.copy()

    with travel(len(metrics)):
      dispatcher.dispatch()

    assert buffer == dispatcher.buffer

    request = httpretty.last_request()

    assert request.headers.get("Content-Type") == "application/json"
    assert request.headers.get("User-Agent") == "Autoscale Agent (Python)"
    assert request.headers.get("Autoscale-Metric-Token") == TOKEN

    actual_body = json.loads(request.body.decode('utf-8'))
    expected_body = {
        "946684801": 1,
        "946684802": 2,
        "946684803": 3,
        "946684804": 4,
        "946684805": 5,
        "946684806": 6
    }

    assert actual_body == expected_body

    out, _ = capsys.readouterr()

    assert "Autoscale::Agent/WebDispatcher[u4quBFg][ERROR]: Failed to dispatch (500)" in out

def test_prune():
    dispatcher = WebDispatcher(TOKEN)

    with travel(-61):
        dispatcher.add(1)

    dispatcher.add(2)

    assert dispatcher.buffer == {946684739: 1, 946684800: 2}

    dispatcher.prune()

    assert dispatcher.buffer == {946684800: 2}
