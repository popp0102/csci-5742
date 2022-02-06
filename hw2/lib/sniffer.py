import time
import random

class Sniffer(object):
    def __init__(self, connection_table):
        self.connection_table = connection_table

    def sniff(self):
        while(1):
            print("(sniffer thread) sniffing...")
            random_source_ip = str(random.randint(1, 100))
            destination_ip   = "10"
            destination_port = 10
            self.connection_table.add(random_source_ip, destination_ip, destination_port)
            time.sleep(0.5)

