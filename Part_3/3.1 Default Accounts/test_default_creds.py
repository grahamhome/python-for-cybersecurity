import asyncio

import paramiko
import telnetlib3

"""
Check for the existence of SSH and Telnet accounts with known credentials.
"""


def SSHLogin(host, username, password, port=22):
    """
    Attempts to open a SSH connection to the given host at the given port and authenticate
    with the given username and password.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print(
                "Login successful on %s:%s with username %s and password %s"
                % (host, port, username, password)
            )
    except:
        print("Login failed %s %s" % (username, password))
    finally:
        ssh.close()


def TelnetLogin(host, port, username, password):
    """
    Attempts to log in to Telnet using given credentials.
    """

    async def attempt_login(reader, writer):
        """
        Attempts to log in to Telnet.
        """
        # await reader.readuntil(b"login: ")
        print(await reader.read(1024), flush=True)
        writer.write(username + "\n")
        await reader.readuntil(b"Password: ")
        writer.write(password + "\n")
        try:
            reader.readuntil(b"Last login")
            print(
                "Telnet login successful on %s:%s with username %s and password %s"
                % (host, port, username, password)
            )
        except:
            print("Login failed %s %s" % (username, password))
        finally:
            writer.close()

    loop = asyncio.get_event_loop()
    coro = telnetlib3.open_connection(host, port, shell=attempt_login)
    reader, writer = loop.run_until_complete(coro)
    loop.run_until_complete(writer.protocol.waiter_closed)


host = "localhost"
port = "6023"
with open("defaults.txt", "r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host=host, username=username, password=password)
        TelnetLogin(host, port, username, password)
