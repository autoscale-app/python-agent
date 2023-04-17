class WorkerServer:
    def __init__(self, token, callable):
        self.token = token
        self._callable = callable

    def serve(self):
        return self._callable()
