from scapy.all import *

"""
Transmits data disguised as ICMP packets. Covert transmission but limited to 1 character/packet
so not suitable for large transmissions.s
"""

def transmit(message, host):
    for m in message:
        packet = IP(dst=host) / ICMP(code=ord(m))
        send(packet)


# Use local host for testing
host = "172.28.48.1"
message = "Hello"
transmit(message, host)
