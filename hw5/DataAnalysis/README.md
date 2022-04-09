# Data Analytics
This project is a small python3 script that pulls in a pcap file, parses it
and outputs a csv with a subset of the information.  
These files use the external libraries Pandas and Scapy, both are required to
run the script. A requirements.txt has been provided, feel free to install the
required packages via `pip install -r requirements.txt`

## Usage
`python3 Tables.py input.pcap --output out.csv`