from random import randint
from socket import socket, AF_PACKET, SOCK_RAW, htons
from struct import unpack
from time import sleep


class Sniffer(object):
    def __init__(self, connection_table):
        ETH_P_ALL = 3  # GET ALL PACKETS FROM PHYSICAL LAYER
        self.connection_table = connection_table

        self.s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))
        self.should_listen = False

    def listen(self):
        self.should_listen = True
        while self.should_listen:
            data, address = self.s.recvfrom(65536)
            dest_mac, src_mac, protocol = unpack('!6s6sH', data[:14])
            print(f'Interface = {address[0]}')
            print(f'{self.to_ethernet_protocol_string(protocol)}')
            body = data[14:]

    @staticmethod
    def dissect_ipv4_header(body):
        ip_protocol, source_ip, target_ip = unpack('!9x B 2x 4s 4s', body[:20])

    @staticmethod
    def to_ethernet_protocol_string(protocol_enum):
        protocol_string = "Unknown"
        if protocol_enum == 0x0800:
            protocol_string = "IPv4"
        elif protocol_enum == 0x0806:
            protocol_string = "ARP"
        elif protocol_enum == 0x0842:
            protocol_string = "WoL"
        elif protocol_enum == 0x22F0:
            protocol_string = "AVTP"
        elif protocol_enum == 0x22F3:
            protocol_string = "TRILL"
        elif protocol_enum == 0x22EA:
            protocol_string = "SRP"
        elif protocol_enum == 0x6002:
            protocol_string = "DEC MOP RC"
        elif protocol_enum == 0x86DD:
            protocol_string = "IPv6"
        return protocol_string

    def sniff(self):
        while self.should_listen:
            print("(sniffer thread) sniffing...")
            random_source_ip = str(randint(1, 100))
            destination_ip = "10"
            destination_port = 10
            self.connection_table.add(random_source_ip, destination_ip, destination_port)
            sleep(0.5)
