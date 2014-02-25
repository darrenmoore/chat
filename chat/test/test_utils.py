import sys, os
import unittest
import socket
import time
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

class TestUtils(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_generate_token(self):
		token = generate_token()
		self.assertTrue(len(token) == 36)

	def test_generate_token_short(self):
		token = generate_token(type='short')
		self.assertTrue(len(token) == 8)

if __name__ == '__main__':
  unittest.main()