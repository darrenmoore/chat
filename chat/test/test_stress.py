import sys, os
import unittest
import socket
import time

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client

class TestStress(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_second_system(self):
		start = time.strftime('%S')
		count = 0
		while start == time.strftime('%S'):
			count = count+1
		print "%s calls per second" % str(count)
		self.assertTrue(count > 100000)

	def test_second_ping(self):
		self.client = Client()
	 	self.client.connect_db()
		start = time.strftime('%S')
		count = 0
		while start == time.strftime('%S'):
			count = count+1
			result = self.client.send(b'ping')
		print "%s calls per second" % str(count)
		self.client.connection.close()
		self.assertTrue(count > 1000)

if __name__ == '__main__':
  unittest.main()