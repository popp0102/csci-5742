class ConnectionTable():
    def __init__(self):
        self.table = {}

    def add(self, src_ip, dest_ip, dest_port):
        self.table[src_ip] = 1

    def size(self):
        return len(self.table)

