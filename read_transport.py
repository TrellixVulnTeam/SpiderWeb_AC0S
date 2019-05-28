import threading
from scapy.all import *
from utils import get_ip


class Reader:
    def __init__(self):
        ip = get_ip()
        port_to_service_table = {
            80: "http/http\'s",
            443: "http\'s",
            21: "ftp",
            25: "smtp",
            53: "dns"
        }
