#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP/IP range ")
    option = parser.parse_args()
    return option


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcust = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcust = broadcust / arp_request
    answer_list = scapy.srp(arp_request_broadcust, timeout=1, verbose=False)[0]
    client_list = []
    for elements in answer_list:
        client_dict = {"ip": elements[1].psrc, "mac": elements[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(result_list):
    print("IP\t\t\tMAC Adress\n-------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


option = get_argument()
scan_result = scan(option.target)
print_result(scan_result)
