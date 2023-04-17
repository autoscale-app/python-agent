import json
import time
import http.client
import autoscale_agent.request as request

class WorkerDispatcher:
    def __init__(self, token, block):
        self.token = token
        self.id = token[:7]
        self.block = block

    def dispatch(self):
        value = self.block()

        if value:
            body = json.dumps({int(time.time()): value})
            response = request.dispatch(body=body, token=self.token)

            if response.status != http.client.OK:
                error_msg = f"Failed to dispatch ({response.status}) {response.read().decode()}"
                self.error(error_msg)
        else:
            self.error("Failed to calculate worker information (None)")

    def error(self, msg):
        print(f"Autoscale::Agent/WorkerDispatcher[{self.id}][ERROR]: {msg}")
