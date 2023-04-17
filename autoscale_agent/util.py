import http.client
import os


def debug(*args, **kwargs):
    if os.getenv("AUTOSCALE_DEBUG"):
        print(*args, **kwargs)


def dispatch(body, token):
    headers = {
        "User-Agent": "Autoscale Agent (Python)",
        "Autoscale-Metric-Token": token,
        "Content-Type": "application/json",
    }
    body_bytes = body.encode("utf-8")
    conn = http.client.HTTPSConnection("metrics.autoscale.app", timeout=5)
    conn.request("POST", "/", body=body_bytes, headers=headers)
    response = conn.getresponse()
    conn.close()
    return response
