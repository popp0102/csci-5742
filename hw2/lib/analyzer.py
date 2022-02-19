from datetime import datetime
import time
import logging

class Analyzer(object):
    ONE_MINUTE   = 60
    FIVE_MINUTES = 300

    def __init__(self, second_threshold, minute_threshold, five_minute_threshold, connection_table):
        self.sec_threshold      = second_threshold
        self.min_threshold      = minute_threshold
        self.five_min_threshold = five_minute_threshold
        self.connection_table   = connection_table
        self.fanout_rates       = {}

    def analyze(self):
        now               = datetime.now()
        second_start      = now
        minute_start      = now
        five_minute_start = now
        while(1):
            now = datetime.now()
            self.calculate_fanout_rates(minute_start, second_start, now)
            self.display_detected_port_scanners()

            second_start = now
            minute_start = now if (now - minute_start).seconds >= self.ONE_MINUTE else minute_start
            logging.debug(f"Connection Size: {self.connection_table.size()}")
            if (now - five_minute_start).seconds >= self.FIVE_MINUTES:
                self.connection_table.vacuum(five_minute_start)
                five_minute_start = now
            time.sleep(1)

    def calculate_fanout_rates(self, minute_start, start, end):
        sources = self.connection_table.get_sources()

        for source in sources:
            fanout_rate_per_second  = self.calculate_fanout_rate_per_second(source, start, end)
            fanout_rate_per_minute  = self.calculate_fanout_rate_per_minute(source, minute_start, end)
            fanout_rate_per_5minute = self.calculate_fanout_rate_per_5minute(source)

            self.fanout_rates.setdefault(source, {'displayed': False})
            self.fanout_rates[source]['second']  = fanout_rate_per_second
            self.fanout_rates[source]['minute']  = fanout_rate_per_minute
            self.fanout_rates[source]['5minute'] = fanout_rate_per_5minute


    def calculate_fanout_rate_per_second(self, source, start, end):
        num_connections = self.connection_table.get_num_connections_in_range(source, start, end)
        time_delta      = end - start
        seconds_past    = time_delta.seconds
        fanout_rate     = num_connections / seconds_past if seconds_past >= 1 else num_connections
        return int(fanout_rate)

    def calculate_fanout_rate_per_minute(self, source, start, end):
        num_connections = self.connection_table.get_num_connections_in_range(source, start, end)
        time_delta      = end - start
        minutes_past    = time_delta.seconds / 60
        fanout_rate     = num_connections / minutes_past if minutes_past >= 1 else num_connections
        return int(fanout_rate)

    def calculate_fanout_rate_per_5minute(self, source):
        num_connections = self.connection_table.get_num_connections_in_range(source, None, None)
        return int(num_connections)

    def display_detected_port_scanners(self):
        for source, fanout_rates in self.fanout_rates.items():
            reason = None
            if fanout_rates['second'] >= self.sec_threshold:
                reason = self.get_reason_str('second', fanout_rates['second'], self.sec_threshold)
            elif fanout_rates['minute'] >= self.min_threshold:
                reason = self.get_reason_str('minute', fanout_rates['minute'], self.min_threshold)
            elif fanout_rates['5minute'] >= self.five_min_threshold:
                reason = self.get_reason_str('5 minutes', fanout_rates['5minute'], self.five_min_threshold)

            if reason:
                self.log_detected_scanner(source, reason, fanout_rates)

    def get_reason_str(self, rate_str, rate, threshold):
        return f"fanout rate per {rate_str}={rate} (must be less than {threshold})"

    def log_detected_scanner(self, source, reason, fanout_rates):
        banner           = "-----------------------------------------------"
        detected_str     = f"port scanner detected on {source: <10}"
        fanout_rates_str = f"{fanout_rates['second']}/s|{fanout_rates['minute']}/m|{fanout_rates['5minute']}/5m"
        output_str       = f"{banner}\n{detected_str}\n->\tfanout rates: {fanout_rates_str} \n->\treason: {reason}\n{banner}"

        # Only display the detection once
        if not fanout_rates['displayed']:
            fanout_rates['displayed'] = True
            logging.info(output_str)

