import os
import re
from zipfile import ZipFile

# Easily add new regexes for other types of PII e.g. CC numbers
email_regex = "[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}"
phone_regex = "[(]*[0-9]{3}[)]*-[0-9]{3}-[0-9]{4}"
ssn_regex = "[0-9]{3}-[0-9]{2}-[0-9]{4}"
regexes = [email_regex, phone_regex, ssn_regex]


def findPII(data):
    """
    Checks for email addresses, phone numbers and SSNs in document contents.
    """
    matches = []
    for regex in regexes:
        m = re.findall(regex, data)
        matches += m
    return matches


def printMatches(filedir, matches):
    """
    Prints a file directory and all the PII contained in that file.
    """
    if len(matches) > 0:
        print(filedir)
        for match in matches:
            print(match)


def parseDocx(root, docs):
    """
    Read in the contents of a Word document and check for PII.
    """
    for doc in docs:
        matches = None
        filedir = os.path.join(root, doc)
        with ZipFile(filedir, "r") as zip:
            data = zip.read("word/document.xml")
            matches = findPII(data.decode("utf-8"))
        printMatches(filedir, matches)


def parseText(root, txts):
    """
    Reads in a text file and checks for PII.
    """
    for txt in txts:
        filedir = os.path.join(root, txt)
        with open(filedir, "r") as f:
            data = f.read()
        matches = findPII(data)
        printMatches(filedir, matches)


txt_ext = [".txt", ".py", ".csv"]


def findFiles(directory):
    """
    Finds all Word docs and text files on the filesystem within the given directory.
    Does not recurse into subfolders.
    """
    for root, dirs, files in os.walk(directory):
        parseDocx(root, [f for f in files if f.endswith(".docx")])
        for ext in txt_ext:
            parseText(root, [f for f in files if f.endswith(ext)])


directory = os.path.join(os.getcwd(), "Documents")
findFiles(directory)
