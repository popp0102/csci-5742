#!./venv/bin/python

from lib.command_line_parser import cmd_parse
from lib.sniffer             import Sniffer
from lib.analyzer            import Analyzer

def main():
    args       = cmd_parse()
    sniffer    = Sniffer()
    analyzer   = Analyzer(args.fps, args.fpm, args.fp5m)

if __name__ == "__main__":
    main()

