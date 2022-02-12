import time
import logging

class Analyzer(object):
    def __init__(self, second_threshold, minute_threshold, five_minute_threshold, connection_table):
        self.sec_threshold      = second_threshold
        self.min_threshold      = minute_threshold
        self.five_min_threshold = five_minute_threshold
        self.connection_table   = connection_table

    def analyze(self):
        while(1):
            logging.info(f"(analyzer thread): {self.connection_table.size()} entries in the connection table")
            time.sleep(1)

