#!/usr/bin/env python
# -*- mode: python; coding: utf-8-unix -*- 
import sys
import os
import smtplib
import email
import pprint
from email.utils import getaddresses
import poplib
import time

server = '192.168.127.60'
port = 25

from sets import Set
emails=Set([])

def delete_from_email(email):
    server = "192.168.127.10"
    port = 110
    user = email
    passwd = "<secret_password>"
    
    pop = poplib.POP3(server, port)
    pop.user(user)
    pop.pass_(passwd)
    
    poplist = pop.list()
    if poplist[0].startswith('+OK') :
        msglist = poplist[1]
        for msgspec in msglist :
            # msgspec is something like "3 3941", 
            # msg number and size in octets
            msgnum = int(msgspec.split(' ')[0])
            print "Deleting msg %d\r" % msgnum,
            pop.dele(msgnum)
        else :
            print "No messages for", user
    else :
        print "Couldn't list messages: status", poplist[0]
    pop.quit()
    
while True:
  for fn in os.listdir('sample_emails'):
    time.sleep(1)
    print "iterating over: " + fn
    if os.path.isfile('sample_emails/'+fn):
        with open('sample_emails/'+fn) as f:
            
            message = f.read()
            msg = email.message_from_string(message)
            mailfrom=email.utils.parseaddr(msg['From'])[1]
            subject=msg['Subject']

            tos=msg.get_all('to', [])
            ccs=ccs = msg.get_all('cc', [])
	    rcpttos = getaddresses(tos)
            cctos = getaddresses(ccs)
            #pprint.pprint (vars(msg))
            recipients=[]
            print "   Sending message from: " + mailfrom
            for rcptto in rcpttos:
                if rcptto is not None:
                    print "   Sending message to:   " + rcptto[1]
                    recipients+=[rcptto[1]]
                    emails.add(rcptto[1])
            for ccto in cctos:
                if ccto is not None:
                    print "   Sending message cc:   " + ccto[1]
                    recipients+=[ccto[1]]
                    emails.add(ccto[1])
            smtp = smtplib.SMTP(server, port)
            smtp.sendmail(mailfrom, recipients, message) 
            print "   Sent."

# get all messages

  for eml in emails:
    eml=eml[0:-4]
    print "Deleting emails for: " + eml
    
    delete_from_email(eml)
