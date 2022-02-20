from datetime import datetime
import logging

class ConnectionTable():
    ############################################################
    # Function: __init__()
    #
    # Constructor for the ConnectionTable class.
    ############################################################
    def __init__(self):
        self.table = {}

    ############################################################
    # Function: add()
    #
    # A method to add a src ip, dest ip and dest port to the
    # table dictionary. It's using a 2d hash.
    ############################################################
    def add(self, src_ip, dest_ip, dest_port):
        if src_ip not in self.table:
            self.table[src_ip] = {}

        dest_connection = dest_ip + dest_port
        if dest_connection not in self.table[src_ip]:
            self.table[src_ip][dest_connection] = datetime.now()

    ############################################################
    # Function: get_sources()
    #
    # Method to return all sources from the table.
    ############################################################
    def get_sources(self):
        return self.table.keys()

    ############################################################
    # Function: get_destinations()
    #
    # Method to return all destinations from the table.
    ############################################################
    def get_destinations(self, source):
        return self.table[source]

    ############################################################
    # Function: get_num_connections_in_range()
    #
    # Given a source, a start time, and an end time return the
    # number of connections in that range.
    ############################################################
    def get_num_connections_in_range(self, source, start, end):
        destinations = self.get_destinations(source)

        if start is None and end is None:
            connections = destinations
        else:
            connections = { source: timestamp for (source, timestamp) in destinations.items() if start <= timestamp and timestamp <= end }

        return len(connections)

    ############################################################
    # Function: size()
    #
    # Method to return the size of the table.
    ############################################################
    def size(self):
        return len(self.table)

    ############################################################
    # Function: vacuum()
    #
    # This method will scan the table and remove all connections
    # that are older than vacuum_time.
    ############################################################
    def vacuum(self, vacuum_time):
        logging.info(f"Vacuuuming Connection Table: removing all entries older than {vacuum_time}...")
        for source, destinations in list(self.table.items()):
            for destination, timestamp in list(destinations.items()):
                if timestamp < vacuum_time:
                    destinations.pop(destination, '')
            if len(destinations) <= 0:
                self.table.pop(source, '')

    ############################################################
    # Function: display()
    #
    # Method to display entries in the connection table.
    ############################################################
    def display(self):
        logging.info("\n-----------------------")
        for source, destinations in self.table.items():
            logging.info(f"source: {source} ({len(destinations)})")
            for destination, timestamp in destinations.items():
                logging.debug(f"  destination: {destination}, timestamp: {timestamp}")
        logging.info("-----------------------")

