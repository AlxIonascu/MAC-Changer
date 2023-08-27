#!/usr/bin/env python

import subprocess
import optparse
import re

"""Gets options from the user in order to set interface and MAC address"""


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to modify")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address for the interface")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    if not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options


"""Changes the MAC address to the new_mac MAC address for the specified interface"""


def change_mac(interface, new_mac):
    print("[+] Changing MAC address to " + new_mac + " for interface " + interface)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


"""gets the current MAC address for the interface given as a parameter"""


def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"..[:]..[:]..[:]..[:]..[:]..", str(ifconfig_output))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("[+] Current MAC is " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address was unsuccessfully changed.")
