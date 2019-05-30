import multiprocessing
from scapy.all import *
from utils import get_ip, Regex


class Reader:
    def __init__(self):
        self.ip = get_ip()
    # writes packets to temporary file
    def packet_writer(self, pkts):
        wrpcap('temp.pcap', pkts)
    # sniffs packets
    def packet_sniffer(self):
        print("[!!!] Starting scan")
        pkts = sniff(filter="ip", count=50)
        self.packet_writer(pkts)
    # sorts packets according to arg given, either with trcroute style or
    # outputs unique ip's found
    def sorter(self, *trcroute):
        pkts = []
        line_num = 0
        raw_packets = rdpcap('temp.pcap')
        if trcroute:
            for pkt in raw_packets:
                mid_pkt = "from {0}:{1} ---> {2}:{3}".format(pkt[IP].src, pkt.sport, pkt[IP].dst, pkt.dport)
                pkts.append(mid_pkt)
        else:
            for pkt in raw_packets:
                pkts.append(pkt[IP].src)
                pkts.append(pkt[IP].dst)

            pkts = list(set(pkts))

        return pkts
