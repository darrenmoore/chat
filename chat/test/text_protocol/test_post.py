import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client
import chat.codes as c

class TestPost(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def test_post_text(self):
		message = 'hello'
		username = self.client.register_login()
		channel = self.client.create_channel()
	 	post = {
	 		'channel': { 'name':channel },
	 		'user': { 'username':username },
	 		'data': message
	 	}
	 	expected = c.post_text(post)
	 	result = self.client.send(b'post %s %s' % (channel, message))
	 	self.assertEqual(expected, result)

	def test_post_multi_channels(self):
		message = 'hello'
		username = self.client.register_login()
		channel = self.client.create_channel()
	 	post = { 'channel': { 'name':channel }, 'user': { 'username':username }, 'data': message }
	 	result = self.client.send(b'post %s %s' % (channel, message))

		channel = self.client.create_channel()
	 	post = { 'channel': { 'name':channel }, 'user': { 'username':username }, 'data': message }
	 	expected = c.post_text(post)
	 	result = self.client.send(b'post %s %s' % (channel, message))

	 	self.assertEqual(expected, result)


	# def test_post_no_such_channel(self):
	#  	pass

	# def test_post_not_joined(self):
	#  	pass

	# def test_post_not_logged_in(self):
	#  	pass

if __name__ == '__main__':
  unittest.main()