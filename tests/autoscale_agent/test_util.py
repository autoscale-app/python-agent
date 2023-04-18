import json
from unittest.mock import MagicMock, patch

from autoscale_agent.util import dispatch


@patch("http.client.HTTPSConnection")
def test_dispatch(mock_conn):
    body = json.dumps({"metric": "worker", "value": 80})
    token = "1234567890"
    mock_response = MagicMock()
    mock_response.status = 200
    mock_conn.return_value.getresponse.return_value = mock_response
    response = dispatch(body, token)
    mock_conn.return_value.request.assert_called_once_with(
        "POST",
        "/",
        body='{"metric": "worker", "value": 80}'.encode("utf-8"),
        headers={
            "User-Agent": "Autoscale Agent (Python)",
            "Content-Type": "application/json",
            "Autoscale-Metric-Token": "1234567890",
        },
    )
    assert response.status == 200
