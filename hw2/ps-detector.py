#!./venv/bin/python

from threading               import Thread
from lib.command_line_parser import cmd_parse
from lib.sniffer             import Sniffer
from lib.analyzer            import Analyzer
from lib.connection_table    import ConnectionTable
import logging



############################################################
# Function: sniff()
#
# A method that executes the sniffer. This method is called
# for one of the 2 threads created from the main method. It's
# job is to sniff traffic and populate the connection table
# with first contact connections.
############################################################
def sniff(connection_table):
    sniffer = Sniffer(connection_table, ["eth0"])
    sniffer.listen()

############################################################
# Function: analyze()
#
# A method that executes the analyzer. This method is called
# for one of the 2 threads created from the main method. It's
# job is to analyze traffic from the sniffer and detect if
# there is a port scanner.
############################################################
def analyze(args, connection_table):
    analyzer = Analyzer(args.fps, args.fpm, args.fp5m, connection_table)
    analyzer.analyze()

############################################################
# Function: main()
#
# The main function that will instantiate all objects and
# run them in 2 main threads - the sniff and the analyze.
# In addition, command line arguments are parsed and passed
# to the appropriate places.
############################################################
def main():
    args      = cmd_parse()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    connection_table = ConnectionTable()
    sniffer_thread   = Thread(target=sniff, args=[connection_table])
    analyzer_thread  = Thread(target=analyze, args=[args, connection_table])

    sniffer_thread.start()
    analyzer_thread.start()

    sniffer_thread.join()
    analyzer_thread.join()


if __name__ == "__main__":
    main()
