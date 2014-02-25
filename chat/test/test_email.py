import sys, os
import unittest
import socket

from mongokit import Document, Connection

sys.path.insert(0, os.path.dirname(__file__))

from chat.utils import *
from chat.emailer import Emailer
from chat.models.email import Email


class TestEmail(unittest.TestCase):

	def setUp(self):
		self.db = Connection()
		self.db.register([Email])
		self.emailer = Emailer(self.db)

	def test_send(self):
		to_email = 'darren@firecreekweb.com'
		subject = 'Test email %s' % random_word()
		template = 'test'
		data = {}
		self.emailer.send(to_email, subject, template, data)
		self.emailer.send_queue()
		email = self.db.Email.find_one({ 'subject':subject, 'status':'sent' })
	 	self.assertTrue(email)

	def test_queued(self):
		to_email = 'darren@firecreekweb.com'
		subject = 'Test email %s' % random_word()
		template = 'test'
		data = {}
		self.emailer.send(to_email, subject, template, data)
		email = self.db.Email.find_one({ 'subject':subject, 'status':'pending' })
		self.emailer.cancel_queue()
	 	self.assertTrue(email)

	def test_cancelled(self):
		to_email = 'darren@firecreekweb.com'
		subject = 'Test email %s' % random_word()
		template = 'test'
		data = {}
		self.emailer.send(to_email, subject, template, data)
		self.emailer.cancel_queue()
		email = self.db.Email.find_one({ 'subject':subject, 'status':'cancelled' })
	 	self.assertTrue(email)

if __name__ == '__main__':
  unittest.main()