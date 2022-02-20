import socket
import argparse
import time

############################################################
# Function: cmd_parse()
#
# A method to parse command line arguments and pass them
# back to the caller.
############################################################
def cmd_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="the target ip to do a port scan on", type=str, required=True)
    parser.add_argument("-w", "--wait",  help="every 2 scans of a port wait this amount of time (in milliseconds)", type=int, required=True)

    return parser.parse_args()

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
  for portNumber in range(1, 1024):
    if tcp_scanner(target, portNumber):
      print('[*] Port', portNumber, '/tcp','is open')
    count = (count + 1) % 2
    if count == 0:
        time.sleep(waitms / 1000)

if __name__ == "__main__":
  main()

