import sys, os
import unittest
import socket
from chat.utils import *
from chat.test.client import Client

sys.path.insert(0, os.path.dirname(__file__))


class TestPost(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def test_post_text(self):
		message = 'hello'
		channel = random_channel()
		username = self.client.register_login()
	 	result = self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'join %s' % channel)
	 	post = {
	 		'channel': { 'name':channel },
	 		'user': { 'username':username },
	 		'data': message
	 	}
	 	result = self.client.send(b'post %s %s' % (channel, message))
	 	print result
	 	#self.assertEqual(expected, result)

	# def test_post_multi_channels(self):
	# 	message = 'hello'
	# 	username = self.client.register_login()
	# 	channel = self.client.create_channel()
	#  	post = { 'channel': { 'name':channel }, 'user': { 'username':username }, 'data': message }
	#  	result = self.client.send(b'post %s %s' % (channel, message))

	# 	channel = self.client.create_channel()
	#  	post = { 'channel': { 'name':channel }, 'user': { 'username':username }, 'data': message }
	#  	expected = c.post_text(post)
	#  	result = self.client.send(b'post %s %s' % (channel, message))

	#  	self.assertEqual(expected, result)


	# def test_post_no_such_channel(self):
	#  	pass

	# def test_post_not_joined(self):
	#  	pass

	# def test_post_not_logged_in(self):
	#  	pass

if __name__ == '__main__':
  unittest.main()