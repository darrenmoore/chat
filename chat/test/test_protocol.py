import sys, os
import unittest
import socket

sys.path.insert(0, os.path.dirname(__file__))

from chat.protocol import Protocol
import chat.codes as c

class TestProtocol(unittest.TestCase):

	def setUp(self):
		self.Protocol = Protocol()
		pass

	def test_text_plain(self):
		result = self.Protocol.output('text', c.TEST_PLAIN)
		self.assertEqual(b'success', result)

	def test_text_format(self):
		data = {
			"stringa": "Foo",
			"stringb": "Bar"
		}
		result = self.Protocol.output('text', c.TEST_FORMAT, data=data)
		self.assertEqual(b'Test Foo Bar', result)



if __name__ == '__main__':
  unittest.main()