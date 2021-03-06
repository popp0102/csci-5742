import socket
import argparse
import time
from datetime import datetime

############################################################
# Function: cmd_parse()
#
# A method to parse command line arguments and pass them
# back to the caller.
############################################################
def cmd_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="the target ip to do a port scan on (IPv4 notation)", type=str, required=True)
    parser.add_argument("-w", "--wait",  help="every 2 scans of a port wait this amount of time (in milliseconds)", type=int, required=True)

    args = parser.parse_args()
    validate_target(args.target)
    return args

############################################################
# Function: usage()
#
# This method takes in a string to print as an error and
# then prints out the correct form of the input that should
# be entered by the user
############################################################
def usage(input_str):
    print("\nError: {}".format(input_str))
    print("target should be of the form 'a.b.c.d' where a,b,c, and d are [0-255]\n")
    exit()

############################################################
# Function: validate_target()
#
# This method takes in the user input and validates the input
# is of the correct format. If it isn't, the program will exit
# telling the user that the format was incorrect. It will then
# provide usage details on how to put a correct format in.
############################################################
def validate_target(ip):
    ip_pieces = ip.split('.')
    if len(ip_pieces) != 4:
        usage("IP Address portion must have 4 pieces separated by a .")

    for ip_piece in ip_pieces:
        if not ip_piece.isnumeric():
            usage("IP must be a number")
        ip_piece_int = int(ip_piece)
        if ip_piece_int > 255 or ip_piece_int < 0:
            usage("IP pieces must be a number 0-255")

####################################################################
# Function: tcp_scanner()
#
# Description: This method will receive an IP and port number and
# attempt to start a TCP connection. If it successfuly creates one
# then it will close the connection (socket) and return True
# otherwise it will catch an exception thrown if it was not
# successful and return False
####################################################################
def tcp_scanner(target, port):
  try:
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((target, port))
    tcp_sock.close()
    return True
  except:
    return False

####################################################################
# Function: main()
#
# Description: main method. It will take in command line arguments
# for the wait time and the target ip. Then it will do a TCP port
# scan from ports 1-1023. Only TCP is scanning is supported for
# this lab as per the professor. Finally, it will print if the port
# is open or closed based on the methods defined above.
####################################################################
def main():
  args   = cmd_parse()
  target = args.target
  waitms = args.wait
  count  = 0
  for port_number in range(1, 1024):
    if tcp_scanner(target, port_number):
      print('[*] Port', port_number, '/tcp','is open')
    if count % 2 == 0:
        time.sleep(waitms / 1000)
        if count % 100 == 0:
            count = 0
            upper_port = port_number + 100
            upper_port = upper_port if upper_port <= 1023 else 1023
            print(f'[*] ({datetime.now()}) Checking Ports {port_number} - {upper_port}')
    count += 1

if __name__ == "__main__":
  main()

