from datetime import datetime

class ConnectionTable():
    def __init__(self):
        self.table = {}

    def add(self, src_ip, dest_ip, dest_port):
        if src_ip not in self.table:
            self.table[src_ip] = {}

        dest_connection = dest_ip + dest_port
        if dest_connection not in self.table[src_ip]:
            self.table[src_ip][dest_connection] = datetime.now()

    def size(self):
        return len(self.table)

