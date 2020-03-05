# This is the command line utility for returning scams to scammers

import win32com.client
import win32com
import requests
import json
import re
import random
import pickle
import SpamCloggerMessageResponses
import os
import sys
from datetime import datetime
import datetime
import os
import google_message
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from google.cloud import storage
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file("spamclogger-5dd55ad0a65c.json")

f = open("testfile.txt", "w+")

JUNK_FOLDER_NAME = "Junk Email"
SPAM_LIST = ['RBC.RoyalBank.Customer.Service.CANADA0780AVX0780@mail186-26.suw21.mandrillapp.com',
             'elhaabundia@gmail.com', 'qq79@edkomb.com',"account@equifax.ca"]

def create_potential_scam_emails(email_list):
    url = 'http://127.0.0.1:8000/api/create-potential-scam-emails'
    myobj = random.sample(email_list, 10)
    myobj = json.dumps(myobj)
    print(requests.post(url, data=myobj).json())

def flood_form(the_url):
    url = 'http://127.0.0.1:7000/api/generate-code'
    myobj = the_url[0]
    myobj = json.dumps(myobj)
    result = requests.post(url, data=myobj).json()
    bot = webdriver.Chrome()
    bot.get(the_url[0])
    time.sleep(5)
    bot.save_screenshot('screenie.png')
    email = bot.find_element_by_name('userId')
    password = bot.find_element_by_name('pin')

    email.clear()
    password.clear()
    email.send_keys(result["email"])
    password.send_keys(result["password"])
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    bot.close()

def scam_different_email(email, outlook, scam):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = "scraddich@yopmail.com"
    mail.Subject = random.choice(SpamCloggerMessageResponses.MESSAGE_TITLES)
    mail.Body = google_message.generate_message(scam.Body)
    mail.Send()

def determine_scam_type(email, account):
    pass

def create_scam_emails():
    url = 'http://127.0.0.1:8000/api/create-scam-emails'
    myobj = SPAM_LIST
    myobj = json.dumps(myobj)
    print(requests.post(url, data=myobj).json())


def get_junk_inbox(outlook):
    for i in range(50):
        try:
            box = outlook.GetDefaultFolder(i)  # Junk Mail is currently email folder 23
            if box.Name == JUNK_FOLDER_NAME:
                return [i, box.Name]
        except:
            pass


def decide_if_email_spam(email):
    if "I am a banker" in email.Body:
        return True
    if "legitimate transaction" in email.Body:
        return True
    if "Attention: Beneficiary" in email.Body:
        return True

    return False


def extract_junk_mail_emails(folder, account):
    ''' try:
         date = pickle.load(open("date.p", "rb"))
     except:
         date = datetime.now() - datetime.timedelta(days=3*365)
     '''
    messages = folder.Items
    list_of_emails = []
    number_of_emails = len(messages)
    if number_of_emails > 0:
        for message2 in messages:
            #if message2.ReceivedTime:
                try:
                    sender = message2.SenderEmailAddress
                    message = message2.Subject
                    body = message2.ReceivedTime
                    if sender != "":
                        list_of_emails.append(sender)
                except:
                    pass
    else:
        return []
    url = 'http://127.0.0.1:8000/api/send-emails'
    myobj = list_of_emails
    myobj = json.dumps(myobj)
    #create_potential_scam_emails(list_of_emails)
    verified_scams = requests.post(url, data=myobj).json()
    scam_messages = []
    for message in messages:
        try:
            if str(message.SenderEmailAddress) in verified_scams:
                scam_messages.append(message)
        except:
            pass

    #now = datetime.datetime.now()
    #pickle.dump(now, open("date.p", "wb"))
    return scam_messages


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts = win32com.client.Dispatch("Outlook.Application").Session.Accounts

inbox = outlook.Folders(accounts[0].DeliveryStore.DisplayName)
folders = inbox.Folders

create_scam_emails()
scam_emails = []
for folder in folders:
    if str(folder) == get_junk_inbox(outlook)[1]:
        scam_emails = (extract_junk_mail_emails(folder, accounts[0]))

for scam in scam_emails:
    addresses_found = re.findall("([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",scam.Body)
    for address in addresses_found:
        if address.lower() != accounts[0].DeliveryStore.DisplayName.lower():
            #scam_different_email(address, accounts[0], scam)
            pass
        else:
            pass
    if ("equifax" in scam.Body.lower()):
        flood_form(re.findall("\<(.*?)\>",scam.Body))


