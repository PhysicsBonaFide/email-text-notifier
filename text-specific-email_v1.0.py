import imaplib
import email
import time
from twilio.rest import Client

#create a Twilio account and get a phone number
account_sid = 'Twilio_SID'
auth_token = 'Twilio_Auth_Token'
client = Client(account_sid, auth_token)

def ReadMail():
    username = 'email@email.com'
    #make an app password on google account security settings (select custom, make a name, and then generate)
    app_password = 'app_password'

    gmail_host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    mail.login(username, app_password)

    mail.select("INBOX")

    sender = False

    #take out 'UNSEEN' if you want to search all emails from the sender, not just unread ones
    _, selected_mails = mail.search(None, '(FROM "sender@email.com")', 'UNSEEN')

    if len(selected_mails[0].split()) > 0:
        sender = True

    print(sender)

    mail.logout()

    if sender == True:
        SendText(sender)

def SendText(sender):
    #reason for redundancy of the if statement is because this allows the program to be expand to search for different people and send individual texts
    if sender == True:
        message = client.messages \
            .create(
            body="Put the body of your message here.",
            from_='+twilio_phone_number',
            to='+your_phone_number'
        )
        print(message.sid)

#Prints the emails, for future reference
'''
for num in selected_mails[0].split():
    _, data = mail.fetch(num , '(RFC822)')
    _, bytes_data = data[0]

    #convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    print("\n===========================================")

    #access data
    print("Subject: ",email_message["subject"])
    print("To:", email_message["to"])
    print("From: ",email_message["from"])
    print("Date: ",email_message["date"])
    for part in email_message.walk():
        if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
            message = part.get_payload(decode=True)
            print("Message: \n", message.decode())
            print("==========================================\n")
            break
'''

while 1:
    ReadMail()
    #change the number if you want it to run on a longer or shorter interval
    time.sleep(7200)
