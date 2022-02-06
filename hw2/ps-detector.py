#!./venv/bin/python

from threading               import Thread
from lib.command_line_parser import cmd_parse
from lib.sniffer             import Sniffer
from lib.analyzer            import Analyzer
from lib.connection_table    import ConnectionTable

def sniff(connection_table):
    sniffer = Sniffer(connection_table)
    sniffer.sniff()

def analyze(args, connection_table):
    analyzer = Analyzer(args.fps, args.fpm, args.fp5m, connection_table)
    analyzer.analyze()

def main():
    args             = cmd_parse()
    connection_table = ConnectionTable()

    sniffer_thread  = Thread(target=sniff, args=[connection_table])
    analyzer_thread = Thread(target=analyze, args=[args, connection_table])

    sniffer_thread.start()
    analyzer_thread.start()

    sniffer_thread.join()
    analyzer_thread.join()

if __name__ == "__main__":
    main()

