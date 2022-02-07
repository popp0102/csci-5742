class ConnectionTable():
    def __init__(self):
        self.table = {}

    def add(self, src_ip, dest_ip, dest_port):
        key = src_ip + dest_ip + dest_port
        if key in self.table:
            self.table[key] += 1
        else:
            self.table[key] = 1

    def size(self):
        return len(self.table)

