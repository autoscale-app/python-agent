class WorkerServer:
    def __init__(self, token, block):
        self.token = token
        self.block = block

    def serve(self):
        return self.block()
