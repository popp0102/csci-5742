from datetime import datetime
import logging

class ConnectionTable():
    def __init__(self):
        self.table = {}

    def add(self, src_ip, dest_ip, dest_port):
        if src_ip not in self.table:
            self.table[src_ip] = {}

        dest_connection = dest_ip + dest_port
        if dest_connection not in self.table[src_ip]:
            self.table[src_ip][dest_connection] = datetime.now()

    def get_sources(self):
        return self.table.keys()

    def get_destinations(self, source):
        return self.table[source]

    def get_num_connections_in_range(self, source, start, end):
        destinations = self.get_destinations(source)

        if start is None and end is None:
            connections = destinations
        else:
            connections = { source: timestamp for (source, timestamp) in destinations.items() if start <= timestamp and timestamp <= end }

        return len(connections)

    def get_destinations(self, source):
        return self.table[source]

    def display(self):
        logging.info("\n-----------------------")
        for source, destinations in self.table.items():
            logging.info(f"source: {source} ({len(destinations)})")
            for destination, timestamp in destinations.items():
                logging.debug(f"  destination: {destination}, timestamp: {timestamp}")
        logging.info("-----------------------")

