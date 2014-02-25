import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))


class TestParseUrl(unittest.TestCase):

	def setUp(self):
		pass

	def test_url(self):
		url = '/users/whoami';
		expected = { 'controller':'users','action':'whoami','params':{} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)

	def test_url_trailing(self):
		url = '/users/whoami/';
		expected = { 'controller':'users','action':'whoami','params':{} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)

	def test_url_one_param(self):
		url = '/users/whoami?foo=bar';
		expected = { 'controller':'users','action':'whoami','params':{'foo':'bar'} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)

	def test_url_one_param_trailing(self):
		url = '/users/whoami/?foo=bar';
		expected = { 'controller':'users','action':'whoami','params':{'foo':'bar'} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)

	def test_url_two_params(self):
		url = '/users/whoami?foo=bar&jane=joe';
		expected = { 'controller':'users','action':'whoami','params':{'foo':'bar','jane':'joe'} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)

	def test_url_two_params_trailing(self):
		url = '/users/whoami/?foo=bar&jane=joe';
		expected = { 'controller':'users','action':'whoami','params':{'foo':'bar','jane':'joe'} }
		result = parse_url(url)
	 	self.assertEqual(expected, result)



if __name__ == '__main__':
  unittest.main()