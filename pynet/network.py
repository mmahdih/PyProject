from scapy.all import *

def packet_callback(packet):
    print(packet.summary())

# sniff traffic on interface "eth0"
sniff(iface="eth0", prn=packet_callback, store=10)