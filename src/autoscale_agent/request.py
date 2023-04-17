import http.client
import pprint

def dispatch(body, token):
    print(f"============== Dispatching to metrics.autoscale.app: {body} ==================")

    headers = {
        "User-Agent": "Autoscale Agent (Python)",
        "Autoscale-Metric-Token": token,
        "Content-Type": "application/json"
    }

    print(f"Dispatching to metrics.autoscale.app: {body}")

    body_bytes = body.encode('utf-8')
    conn = http.client.HTTPSConnection("metrics.autoscale.app", timeout=2)
    conn.request("POST", "/", body=body_bytes, headers=headers)
    response = conn.getresponse()

    print(f"Dispatch Status: {response.status} {response.reason}")
    print(f"Dispatch Response: {response.read()}")
    pprint.pprint(vars(response))

    conn.close()
    return response
