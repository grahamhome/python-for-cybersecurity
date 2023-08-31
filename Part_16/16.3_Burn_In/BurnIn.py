import random
from time import sleep

import requests

# Creates network traffic to/from a decoy system. Does not create browser cookies, temp files or
# other local artifacts (Selenium and Chrome could be a better solution for this)

def makeRequest(url):
    _ = requests.get(url)
    return


def getURL():
    return sites[random.randint(0, len(sites) - 1)].rstrip()


clickthrough = 0.5
sleeptime = 1


def browsingSession():
    while random.random() < clickthrough:
        url = getURL()
        makeRequest(url)
        sleep(random.randint(0, sleeptime))


f = open("sites.txt", "r")
sites = f.readlines()

browsingSession()
