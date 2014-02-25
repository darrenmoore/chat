import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client
import chat.codes as c

class TestChannel(unittest.TestCase):

	def setUp(self):
		self.client = Client()
		self.client.register_login()

	def test_create(self):
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual('Created %s' % channel, result)

	def test_create_invalid(self):
		channel = random_word()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_INVALID_NAME'), result)

	def test_create_already_exists(self):
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_ALREADY_EXISTS'), result)

	def test_create_not_logged_in(self):
	 	result = self.client.send(b'logout')
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('NOT_LOGGED_IN'), result)

	def test_list(self):
	 	result = self.client.send(b'list')
	 	self.assertNotEqual(result,'None')

	# def test_join(self):
	# 	name = random_channel()
	#  	result = self.client.send(b'create %s' % name)
	#  	result = self.client.send(b'join %s' % name)
	#  	self.assertEqual(self.client.reply('CHANNEL_JOIN',{ "name":name }), result)

	# def test_part(self):
	# 	name = random_channel()
	#  	result = self.client.send(b'create %s' % name)
	#  	result = self.client.send(b'join %s' % name)
	#  	result = self.client.send(b'part %s' % name)
	#  	self.assertEqual(self.client.reply('CHANNEL_PART',{ "name":name }), result)

	def test_part_not_joined(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'part %s' % name)
	 	result = self.client.send(b'joined')
	 	self.assertEqual(self.client.reply('USER_JOINED_NONE'), result)

	def test_join_not_exist(self):
		name = random_channel()
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_NOT_EXIST', { "name":name }), result)

	def test_joined_already(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_JOINED_ALREADY',{"name":name}), result)

	def test_follow(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_FOLLOW',{"name":name}), result)

	def test_following_already(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_FOLLOWING_ALREADY',{"name":name}), result)

	def test_unfollow(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	result = self.client.send(b'unfollow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW',{"name":name}), result)

	def test_unfollow_not_following(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'unfollow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW_NOT_FOLLOWING',{ "name":name }), result)

	# def test_users(self):
	# 	name = random_channel()
	#  	result = self.client.send(b'create %s' % name)
	#  	result = self.client.send(b'join %s' % name)
	#  	result = self.client.send(b'users %s' % name)
	#  	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW_NOT_FOLLOWING',{ "name":name }), result)

	def test_joined_already(self):
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_JOINED_ALREADY',{ "name":name }), result)


if __name__ == '__main__':
  unittest.main()