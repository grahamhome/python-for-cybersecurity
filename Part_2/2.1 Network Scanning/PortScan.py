from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, TCP, UDP

ports = [25, 80, 53, 443, 445, 8080, 8443]


def SynScan(host):
    """
    Sends a TCP SYN packet to each of the given ports on the host and checks for a SYN/ACK response.
    """
    # sr = Send, wait for reply
    # ans = answered requests, unans = unanswered
    ans, unans = sr(IP(dst=host) / TCP(dport=ports, flags="S"), timeout=2, verbose=0)
    print("Open ports at %s:" % host)
    # Iterate through sent and received packets for ports that responded
    for (
        s,
        r,
    ) in ans:
        # Ensure response packet is TCP
        if s.haslayer(TCP) and r.haslayer(TCP):
            # Verify that response comes from the same port that we sent the packet to
            # (e.g. wasn't intercepted by a firewall or IPS)
            if s[TCP].dport == r[TCP].sport:
                print(s[TCP].dport)


def DNSScan(host):
    """
    Sends a DNS query request via UDP to a host on the default DNS port and checks for a response.
    """
    ans, unans = sr(
        IP(dst=host) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com")),
        timeout=2,
        verbose=0,
    )
    if ans:
        print("DNS Server at %s" % host)


host = "8.8.8.8"

# Here we could choose to loop over a set of known IP addresses for a target
SynScan(host)
DNSScan(host)
