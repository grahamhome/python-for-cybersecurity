from libratom.lib.pff import PffArchive

# Directory varies by host, can be found using current user name and email address
filename = "C:\\Users\\hepos\\Documents\\Outlook Files\\howard@howardposton.com.pst"
archive = PffArchive(filename)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            print("Sender: %s" % message.get_sender_name())
            print("Subject: %s" % message.get_subject())
            print("Message: %s" % message.get_plain_text_body())

# Can now use regex to search for PII and scrape it from the emails