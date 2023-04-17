import pytest
import json
from unittest.mock import patch, MagicMock
import autoscale_agent.request as request

@patch("http.client.HTTPSConnection")
def test_dispatch(mock_conn):
    body = json.dumps({"metric": "worker", "value": 80})
    token = "1234567890"

    # Create a mock response object
    mock_response = MagicMock()
    mock_response.status = 200

    # Set the return value of the getresponse() method on the mock connection object
    mock_conn.return_value.getresponse.return_value = mock_response

    # Call the dispatch function
    response = request.dispatch(body, token)

    # Verify that the request was sent with the expected parameters
    mock_conn.return_value.request.assert_called_once_with(
        "POST",
        "/",
        body='{"metric": "worker", "value": 80}'.encode('utf-8'),
        headers={
            "User-Agent": "Autoscale Agent (Python)",
            "Content-Type": "application/json",
            "Autoscale-Metric-Token": "1234567890"
        }
    )

    # Verify that the response status is 200
    assert response.status == 200
