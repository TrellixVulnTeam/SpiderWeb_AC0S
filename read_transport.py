import multiprocessing
from scapy.all import *
from utils import get_ip
import logging


class Reader:
    def __init__(self):
        self.ip = get_ip()

    def packet_writer(self, pkts):
        wrpcap('temp.pcap', pkts, append=True)

    def packet_sniffer(self):
        pkts = sniff(filter="tcp", prn=Reader.packet_writer)

    def sorter(self):
        pkts = []
        line_num = 0
        raw_packets = rdpcap('temp.pcap')
        for pkt in raw_packets:
            mid_pkt = "from {0}:{1} ---> {2}:{3}".format(pkt.src, pkt.sport, pkt.dst, pkt.dport)
            pkts.append(mid_pkt)
            pkts = list(set(pkts))

        for pkt in pkts:
            print(pkt)
