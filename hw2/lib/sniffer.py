from random import randint
from socket import socket, AF_PACKET, SOCK_RAW, htons
from struct import unpack
from time import sleep
import logging

class Sniffer(object):
    ############################################################
    # Function: __init__()
    #
    # Constructor for the Sniffer class.
    ############################################################
    def __init__(self, connection_table, interfaces):
        ETH_P_ALL = 3  # GET ALL PACKETS FROM PHYSICAL LAYER
        self.connection_table = connection_table

        self.s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))
        self.should_listen = False
        self.interfaces = interfaces

    ############################################################
    # Function: listen()
    #
    # This is the main method of the Sniffer. It listens to traffic
    # on raw sockets. If detects specific protocols and versions
    # on the given interfaces. it will add the source and destination
    # (ip and port) to the connection table.
    ############################################################
    def listen(self):
        self.should_listen = True
        sixteen_bytes = 65536
        while self.should_listen:
            data, address = self.s.recvfrom(sixteen_bytes)
            interface = address[0]
            dest_mac, src_mac, protocol, ethernet_body = self.process_ethernet_frame(data)

            logging.debug(f'Interface = {interface}')
            if interface in self.interfaces:
                logging.debug(f'{self.to_ethernet_protocol_string(protocol)}')
                ip_protocol, source_ip, dest_ip, ip_body = self.process_ethernet_body(ethernet_body, protocol)
                if ip_protocol is None:
                    logging.debug("Unsupported Packet Type, skipping packet...")
                    continue
                source_string = '.'.join(map(str, source_ip))
                dest_string = '.'.join(map(str, dest_ip))
                logging.debug(f'Source IP: {source_string}')
                logging.debug(f'Destination Ip: {dest_string}')
                protocol_string = self.to_packet_protocol_string(ip_protocol)
                logging.debug(f"Ip Protocol: {protocol_string}")
                source_port, dest_port, is_syn_packet, is_tcp, sub_body = self.process_ip_body(ip_body, ip_protocol)
                logging.debug(f"Source Port: {source_port}")
                logging.debug(f"Dest Port: {dest_port}")
                dest_port_string = str(dest_port)
                if source_port is None:
                    logging.debug("No port, continue")
                    continue
                logging.debug(f"(sniffer thread): ({protocol_string}) \
                    {source_string}:{source_port} -> {dest_string}:{dest_port}")
                if not is_tcp or is_tcp and is_syn_packet:
                    logging.debug("Inserting into Table")
                    self.connection_table.add(source_string, dest_string, dest_port_string)

    ############################################################
    # Function: process_ethernet_frame()
    #
    # This method takes in raw data from the socket and returns
    # and parses the destination mac, the source mac, and the
    # protocol version. In addition, it will return the remainder
    # of the message in the frame (aka the datagram).
    ############################################################
    @staticmethod
    def process_ethernet_frame(data):
        header_size = 14
        dest_mac, src_mac, protocol = unpack('!6s6sH', data[:header_size])
        return dest_mac, src_mac, protocol, data[header_size:]

    ############################################################
    # Function: process_ethernet_body()
    #
    # This method takes in the ethernet protocol and body and
    # parses the destination ip, the source ip, and the protocol
    # version. In addition, it will return the remainder
    # of the message in the datagram (aka the TCP segment or
    # UDP datagram).
    ############################################################
    @staticmethod
    def process_ethernet_body(data, ethernet_protocol):
        protocol = None
        source_ip = None
        target_ip = None
        body = data
        if ethernet_protocol == 0x0800: # IPv4
            ipv4_header_length = 20
            protocol, source_ip, target_ip = unpack('!9xB2x4s4s', data[:ipv4_header_length])
            body = data[ipv4_header_length:]
        elif ethernet_protocol == 0x86DD: # IPv6
            ipv6_header_length = 40
            protocol, source_ip, target_ip = unpack('!6xB1x16s16s', data[:ipv6_header_length])
            body = data[ipv6_header_length:]
        return protocol, source_ip, target_ip, body

    ############################################################
    # Function: process_ip_body()
    #
    # This method takes in the TCP/UDP data and protocol and
    # parses the destination port, the source port, and the body
    # of the application message.
    ############################################################
    def process_ip_body(self, data, ip_protocol):
        body = data
        source_port = None
        destination_port = None
        is_syn_flag = False
        is_tcp = False
        if ip_protocol == 6:
            is_tcp = True
            source_port, destination_port, flags = unpack('!HH4x4xH', data[:14])
            flags &= 511
            is_syn_flag = self.is_packet_syn_packet_ipv4(flags)
            logging.debug("TCP Packet syn flag: " + str(is_syn_flag))
            body = data[14:]
            logging.debug(f"Source Port: {source_port}, Destination Port: {destination_port}")
        elif ip_protocol == 17:
            source_port, destination_port = unpack('!HH', data[:4])
            logging.debug(f"Source Port: {source_port}, Destination Port: {destination_port}")
            body = data[4:]
        elif ip_protocol == 1:
            logging.debug("ICMP no port")
        return source_port, destination_port, is_syn_flag, is_tcp, body

    ############################################################
    # Function: is_packet_syn_packet_ipv4()
    #
    # Takes in a 2's comp representation of the tcp packet flags
    # Detect if an ip packet is a syn packet
    # Syn packets can either only have the SYN flag set or
    # Can have the CWR and ECE flags set as well.
    ############################################################
    @staticmethod
    def is_packet_syn_packet_ipv4(flags):
        # Flags = [NS|CWR|ECE|URG|ACK|PSH|RST|SYN|FIN]
        return flags == 2 or flags == 194

    ############################################################
    # Function: to_packet_protocol_string()
    #
    # Helper method to translate a protocol enum to a transport
    # layer protocol string.
    ############################################################
    @staticmethod
    def to_packet_protocol_string(protocol_enum):
        protocol_string = "Unknown"
        if protocol_enum == 1:
            protocol_string = "ICMP"
        elif protocol_enum == 6:
            protocol_string = "TCP"
        elif protocol_enum == 17:
            protocol_string = "UDP"
        elif protocol_enum == 27:
            protocol_string = "RDP"
        elif protocol_enum == 41:
            protocol_string = "IPv6"
        return protocol_string

    ############################################################
    # Function: to_ethernet_protocol_string()
    #
    # Helper method to translate a protocol enum to a network
    # layer protocol string.
    ############################################################
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

