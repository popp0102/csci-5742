import time

class Analyzer(object):
    def __init__(self, second_threshold, minute_threshold, five_minute_threshold, connection_table):
        self.sec_threshold      = second_threshold
        self.min_threshold      = minute_threshold
        self.five_min_threshold = five_minute_threshold
        self.connection_table   = connection_table

    def analyze(self):
        while(1):
            print("(analyzer thread) {} entries in the connection table".format(self.connection_table.size()))
            time.sleep(1)

