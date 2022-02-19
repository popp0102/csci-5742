import pdb
import sys
import argparse

def cmd_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action=argparse.BooleanOptionalAction)
    parser.add_argument("-s", "--fps",  help="the fanout rate threshold (per second) that indicates the source is a port scanner (default 5)", type=int, default=5)
    parser.add_argument("-m", "--fpm",  help="the fanout rate threshold (per minute) that indicates the source is a port scanner (default 100)", type=int, default=100)
    parser.add_argument("-l", "--fp5m", help="the fanout rate threshold (per 5 minutes) that indicates the source is a port scanner (default 300)", type=int, default=300)


    return parser.parse_args()

