import socket

import dns
import dns.resolver

"""
Queries domain-level DNS server to determine subdomains and the domain names within each subdomain.
"""

# Set the default DNS server to use
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


def ReverseDNS(ip):
    """
    Performs a reverse DNS query to return the list of domain names belonging to a domain.
    """
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]] + result[1]
    except socket.herror:
        return None


def DNSRequest(domain):
    """
    Performs a DNS lookup on the given domain.
    Prints the domains that are found in the DNS and the domain names within that domain.
    """
    ips = []
    try:
        result = dns.resolver.resolve(domain, raise_on_no_answer=False, tcp=True)
        if result:
            print(domain)
            for answer in result:
                print(answer)
                print("Domain Names: %s" % ReverseDNS(answer.to_text()))
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips


def SubdomainSearch(domain, dictionary, nums):
    """
    Checks for and lists subdomains of a domain from a dictionary.
    """
    successes = []
    for word in dictionary:
        subdomain = word + "." + domain
        DNSRequest(subdomain)
        if nums:
            # Check for subdomains with a number appended to the end e.g. www1.google.com
            for i in range(0, 10):
                s = word + str(i) + "." + domain
                DNSRequest(s)


domain = "google.com"
d = "subdomains.txt"
dictionary = []
with open(d, "r") as f:
    dictionary = f.read().splitlines()
SubdomainSearch(domain, dictionary, True)
