import json
import time
import http.client
import autoscale_agent.request as request


class WorkerDispatcher:
    def __init__(self, token, callable):
        self.token = token
        self.id = token[:7]
        self._callable = callable

    def dispatch(self):
        value = self._callable()

        if not value:
            self.error("Failed to calculate worker information (None)")
            return

        body = json.dumps({int(time.time()): value})
        response = request.dispatch(body=body, token=self.token)

        if not response.status == http.client.OK:
            self.error(
                f"Failed to dispatch ({response.status}) {response.read().decode()}"
            )

    def error(self, msg):
        print(f"Autoscale[{self.id}][ERROR]: {msg}")
