#!/usr/bin/env python
import subprocess
import argparse
import re
import sys

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_option("-i", "--interface", dest="interface", help="[?] Interface for changing MAC")
	parser.add_option("-m", "--mac", dest="new_mac", help="[?] New MAC Address")
	options = parser.parse_args()
	if not options.interface:
		parser.error("[!] Please specify an interface")
	if not options.new_mac:
		parser.error("[!] Please specify a MAC Address")
	return options

def change_mac(interface, mac):
	subprocess.call(["ifconfig"], interface, ["down"])
	subprocess.call(["ifconfig"], interface, ["hw"], ["ether"], mac)
	subprocess.call(["ifconfig"], interface, ["up"])
	print(f"[*] Start changing MAC Address to {mac}")

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] I can't find the MAC Address")
		sys.exit()

options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"[*] Current MAC: {current_mac}")
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.interface:
    print(f"[+] MAC Address was successfully changed to {current_mac}")
else:
    print("[-] MAC Address didn't changed!")