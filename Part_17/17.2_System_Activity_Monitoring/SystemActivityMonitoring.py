import win32evtlog

# Uses Windows Event Log to monitor for failed login attempts in order to help
# detect brute-force and credential-stuffing attacks

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

failures = {}


def checkEvents():
    h = win32evtlog.OpenEventLog(server, logtype)
    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        if events:
            for event in events:
                if event.EventID == 4625: # Failed login attempt event IDs
                    if event.StringInserts[0].startswith("S-1-5-21"): # SID for user accounts (not application accounts)
                        account = event.StringInserts[1]
                        if account in failures:
                            failures[account] += 1
                        else:
                            failures[account] = 1
        else:
            break


checkEvents()

for account in failures:
    print("%s: %s failed logins" % (account, failures[account]))

# Script may be modified to look for failed logins within a specific time period or frequency over time
# Or to look for successful logins outside business hours
