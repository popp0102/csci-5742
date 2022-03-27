from dataclasses import dataclass


@dataclass()
class CapturedPacket:
    # Required
    source_ip: str
    source_port: str
    destination_ip: str
    destination_port: str

    # Included in Context
    raw_http_payload: str
    scan_types: str

    def __init__(self, source_ip: str, source_port: str, destination_ip: str, destination_port: str,
                 raw_http_payload: str = "", scan_types: str = ""):
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.raw_http_payload = raw_http_payload
        self.scan_types = scan_types
