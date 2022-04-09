import argparse
from scapy.utils import rdpcap as read_pcap
from scapy.layers.inet import ICMP, IP, TCP
from pandas import DataFrame, option_context
from CapturedPacket import CapturedPacket


def get_http_payload(tcp_packet):
    """
    Input: TCP Packet
    Output: string representation of the http payload or empty string
    Checks the body of the incoming TCP packet for the value 'http'. If that substring exists, then returns
    the entirety of the tcp body, otherwise, returns and empty string.
    """
    http = 'HTTP'
    response = ''
    tcp_body = str(tcp_packet.payload)
    if http.casefold() in tcp_body:
        response = tcp_body
    return response


def get_packet_scan_type(tcp_packet):
    """
    Input: TCP Packet
    Output: A string representation of the scanning type seen.
    Checks the incoming TCP packet for various bits that are set and returns a name if the packet matches a pattern of
    scan packets
    """
    scan_type_dict = {
        0: 'NULL',
        3: 'SYN-FIN',
        17: 'MAIMON',
        41: 'XMAS'
    }
    response = ''
    flags = tcp_packet.flags.value
    if flags in scan_type_dict:
        response = scan_type_dict[flags]
    return response


def pcap_to_dataframe(packet_list):
    """
    Input: list of SCAPY packets from the rdpcap function
    Output: Pandas DataFrame with ip/port info and scanning info from the pcaps
    """
    data_list = []

    for packet in packet_list:
        if IP in packet:
            ip_packet = packet.getlayer(IP)
            if ICMP in ip_packet:
                new_packet = CapturedPacket(ip_packet.src, '', ip_packet.dst, '')
            else:
                new_packet = CapturedPacket(ip_packet.src, ip_packet.sport, ip_packet.dst, ip_packet.dport)
                if TCP in packet:
                    tmp_tcp_packet = packet.getlayer(TCP)
                    new_packet.scan_types = get_packet_scan_type(tmp_tcp_packet)
                    new_packet.raw_http_payload = get_http_payload(tmp_tcp_packet)
            data_list.append(new_packet)
        else:
            print("Non-ip-packet")
    return DataFrame(data_list)


def main():
    """
    Driver method
    provides commandline parsing and minor business logic switch based on output flag
    """
    parser = argparse.ArgumentParser(description='Process a pcap into a csv')
    parser.add_argument('input_file', help='the location of the pcap file')
    parser.add_argument('--output', help='specifies the output file for the csv', default='commandline')
    args = parser.parse_args()
    output = args.output
    packet_list = read_pcap(args.input_file)
    data_frame = pcap_to_dataframe(packet_list)
    if output == 'commandline':
        with option_context('display.max_rows', 100,
                            'display.max_columns', 6,
                            'display.precision', 3,
                            ):
            print(data_frame)
    else:
        data_frame.to_csv(output)


if __name__ == "__main__":
    main()
