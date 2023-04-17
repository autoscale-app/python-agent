class WorkerServers:
    def __init__(self):
        self.servers = []

    def __iter__(self):
        return iter(self.servers)

    def __len__(self):
        return len(self.servers)

    def __getitem__(self, index):
        return self.servers[index]

    def append(self, server):
        self.servers.append(server)

    def find(self, tokens):
        for server in self.servers:
            if server.token in tokens:
                return server
        return None
