
### linux

# #!/usr/bin/env python3
# from scapy.all import *
# from scapy.layers.dot11 import Dot11, Dot11Elt
#
# ap_list = set()
#
# def PacketHandler(pkt):
#     if pkt.haslayer(Dot11) and pkt.haslayer(Dot11Elt):
#         if pkt.type == 0 and pkt.subtype == 8:
#             ssid = pkt[Dot11Elt].info
#             bssid = pkt.addr2
#             if bssid not in ap_list:
#                 ap_list.add(bssid)
#                 print(f"AP MAC: {bssid} with SSID: {ssid.decode('utf-8')}")
#
# # Update the interface to match your system
# try:
#     iface = conf.iface  # Use the default interface configured in scapy
#     sniff(iface=iface, prn=PacketHandler)
# except ValueError as e:
#     print(f"Error: {e}. Please ensure the wireless interface is available and correct.")



### windows
# import pyshark
#
# def packet_handler(pkt):
#     # if 'wlan' in pkt:
#     print(f"Packet captured: {pkt}")  # Debug: print the packet
#
# # Replace with the correct interface name
# capture = pyshark.LiveCapture(interface=r'\Device\NPF_{40A2B0FB-62C9-4346-B4A8-2990C6A08D7D}')
# capture.apply_on_packets(packet_handler)


#!/usr/bin/env python
# !/usr/bin/env python
import socket
import binascii

# Create raw socket to capture packets
rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

# Bind socket to 'mon0' (ensure your wireless interface is in monitor mode)
rawSocket.bind(("mon0", 0x0003))

ap_list = set()

while True:
    pkt = rawSocket.recvfrom(2048)[0]

    # Check if the packet is a beacon frame (0x80) - Type = 0, Subtype = 8
    if pkt[26] == 0x80:  # Beacon frame check (0x80 is the beacon frame subtype)
        bssid = pkt[36:42]  # Extract BSSID (MAC address of the AP)
        ssid_length = ord(pkt[63])  # Get the SSID length from byte 63

        # Check if SSID is available and add AP to list if not seen before
        if bssid not in ap_list and ssid_length > 0:
            ssid = pkt[64:64 + ssid_length]  # Extract SSID based on length
            ap_list.add(bssid)  # Add BSSID to seen AP list

            # Print SSID and BSSID (convert BSSID to hexadecimal)
            print("SSID: %s  AP MAC: %s" % (ssid.decode('utf-8'), binascii.hexlify(bssid).decode('utf-8')))
