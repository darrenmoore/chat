import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client

class TestChannelSearch(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def tearDown(self):
		self.client.connection.close()

	def test_simple(self):
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	self.client.send(b'search %s' % channel)


if __name__ == '__main__':
  unittest.main()