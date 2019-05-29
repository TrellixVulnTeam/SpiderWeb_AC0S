import multiprocessing
from scapy.all import *
from utils import get_ip, Regex


class Reader:
    def __init__(self):
        self.ip = get_ip()

    def packet_writer(self, pkts):
        wrpcap('temp.pcap', pkts, append=True)

    def packet_sniffer(self):
        print("[!!!] Starting scan")
        pkts = sniff(filter="ip", count=50)
        self.packet_writer(pkts)

    def sorter(self, trcroute):
        pkts = []
        line_num = 0
        raw_packets = rdpcap('temp.pcap')
        if trcroute:
            for pkt in raw_packets:
                mid_pkt = "from {0}:{1} ---> {2}:{3}".format(pkt.src, pkt.sport, pkt.dst, pkt.dport)
                pkts.append(mid_pkt)
        else:
            for pkt in raw_packets:
                pkts.append(pkt.src)
                pkts.append(pkt.dst)

            pkts = list(set(pkts))

        return pkts
