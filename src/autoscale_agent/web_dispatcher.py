import time
import threading
import os


class WebDispatcher:
    TTL = 30

    def __init__(self, token):
        self.id = token[:7]
        self.token = token
        self._buffer = {}
        self._mutex = threading.Lock()

    def dispatch(self):
        payload = self.flush()

        if not payload:
            return

        body = json.dumps(payload)
        response = request.dispatch(body, self.token)

        if not response.status == 200:
            self.revert_payload(payload)

    def add(self, value, timestamp=None):
        with self._mutex:
            now = int(time.time())
            timestamp = timestamp or now

            if timestamp in self._buffer:
                if value > self._buffer[timestamp]:
                    self._buffer[timestamp] = value
            else:
                if timestamp + self.TTL > now:
                    self._buffer[timestamp] = value

    def flush(self):
        with self._mutex:
            payload = self._buffer
            self._buffer = {}
            return payload

    def revert_payload(self, payload):
        for timestamp, value in payload.items():
            self.add(value, timestamp)
