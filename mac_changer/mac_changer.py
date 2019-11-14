#!/usr/bin/env python
import subprocess
import optparse
import re


def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface name to change the mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (option, argument) = parser.parse_args()
    if not option.interface:
        parser.error("[-] Spacify the interface , use --help for more info ")
    elif not option.new_mac:
        parser.error("[-] Spacify the new mac , use --help for more info ")
    return option


def change_mac(interface, mac):
    print("[+] mac is changing for " + interface + " to " + mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_resutl = subprocess.check_output(["ifconfig", interface])
    mac_address_search_resutl = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_resutl)
    if mac_address_search_resutl:
        return mac_address_search_resutl.group(0)
    else:
        print("could not read MAC address")


parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface name to change the mac")
parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
(option, argument) = parser.parse_args()

option = get_argument()
current_mac = get_current_mac(option.interface)
print("Current MAC = "+str(current_mac))
change_mac(option.interface, option.new_mac)
current_mac = get_current_mac(option.interface)
if current_mac == option.new_mac:
    print("[+] MAC was successfully changed to "+current_mac)
else:
    print("[-] MAC address did not changed")
