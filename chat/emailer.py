from utils import *
from models.user import User
from models.email import Email

import smtplib, os


class Emailer(object):

    sessions = {}           #session id, data

    def __init__(self, db):
        self._from_email = 'do-not-reply@heychatapp.com'
        self._from_name = 'Heychatapp'
        self.db = db
        pass

    def send(self, to, subject, template, data, from_email = None, from_name = None):
        filename = '%s/emails/%s.html' % (os.path.dirname(__file__), template)
        fp = open(filename, 'rb')
        body = fp.read()
        fp.close()
        body = str(body)

        if from_email is None:
            from_email = self._from_email

        if from_name is None:
            from_name = self._from_name

        email = self.db.Email()
        email['to_email'] = to
        email['from_email'] = from_email
        email['from_name'] = from_name
        email['subject'] = subject % data
        email['body'] = body % data
        email['status'] = 'pending'
        email.save()
        self.send_queue()

    def send_queue(self):
        email = self.db.Email.find_one({ 'status':'pending' })

        if email is None:
            return

        email['status'] = 'sending'
        email.save()

        message = """From: %(from_name)s <%(from_email)s>
To: %(to_email)s
Subject: %(subject)s

%(body)s
"""
        message = message % email

        s = smtplib.SMTP('localhost')
        s.sendmail(email['from_email'], email['to_email'], message)
        s.quit()

        email['status'] = 'sent'
        email.save()

        self.send_queue()


    def cancel_queue(self):
        self.db.Email.collection.update(
            { 'status': 'pending' }, 
            { '$set': { 'status':'cancelled' } }
        );