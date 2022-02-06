class Analyzer(object):
    def __init__(self, second_threshold, minute_threshold, five_minute_threshold):
        self.sec_threshold      = second_threshold
        self.min_threshold      = minute_threshold
        self.five_min_threshold = five_minute_threshold
        print("Analzyer construction")

