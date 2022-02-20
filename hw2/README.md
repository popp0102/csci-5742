# Requirements
Both the port scanner and the port scanner detector must be run with python version 3.9. This was tested on version 3.9.10 which is the version that came with the Kali Linux VM.

# Quickstart
* Given host 1's IP is 172.16.99.3 and the wait time is 1 ms
* On host 1: sudo python3 ./ps-detector.py
* On host 2: sudo python3 ./port-scanner.py --target 172.16.99.3 --wait 1

# Running the Port Scanner Detector
* sudo python3 ./ps-detector.py
* sudo python3 ./ps-detector.py --help (for help menu and optional arguments)

# Running the Port Scanner
* sudo python3 ./port-scanner.py --target <target ip> --wait <wait time in ms>
* sudo ./ps-detector.py --help (for help menu)

