import signal
import sys
from time import sleep

"""
Decoy process that may be disguised as another process (e.g. AV software).
If terminated by another process, reports the name of this process.

Linux-only.
Unable to catch and respond to SIGKILL signals.
"""


def terminated(signum, frame):
    pass


signal.signal(signal.SIGTERM, terminated)
signal.signal(signal.SIGINT, terminated)
while True:
    siginfo = signal.sigwaitinfo({signal.SIGINT, signal.SIGTERM})
    with open("terminated.txt", "w") as f:
        f.write("Process terminated by %d\n" % siginfo.si_pid)
    sys.exit(0)
