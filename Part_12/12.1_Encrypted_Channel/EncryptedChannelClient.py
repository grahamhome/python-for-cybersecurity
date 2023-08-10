import os
import socket

from Crypto.Cipher import AES

host = "127.0.0.1"
port = 1337

# Symmetric encryption. Victim can recover this key from their system
# and use it to decrypt client-to-server and server-to-client communications.

# Asymmetric encryption would prevent defenders from being able to decrypt
# client-to-server communications, but leaves server-to-client comms vulnerable
# to the target finding the client's public key on their system.

# Encryption simply increases the amount of work necessary for defenders to detect and mitigate a breach.
# Asymmetric encryption can help prevent the defender from seeing what specific data was exfiltrated,
# however, there may be other evidence of this activity on the system.
key = b"Sixteen byte key"


def encrypt(data, key, iv):
    # Pad data as needed
    data += " " * (16 - len(data) % 16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(bytes(data, "utf-8"))


message = "Hello"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    # Initialization vector must be randomly generated for each message so that
    # if the same message is encoded twice with the same key, the ciphertext will be different.
    # (Like salting a hash.) AKA semantic security
    iv = os.urandom(16)
    s.send(iv)
    s.send(bytes([len(message)]))
    encrypted = encrypt(message, key, iv)
    print("Sending %s" % encrypted.hex())
    s.sendall(encrypted)
