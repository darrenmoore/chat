import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client

class TestChannelBan(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def tearDown(self):
		self.client.connection.close()

	def test_ban(self):
		ban_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('CHANNEL_BAN',{ 'name':channel, "username":ban_username }), result)

	def test_ban_not_admin(self):
		channel = random_channel()
		ban_username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
		result = self.client.send(b'logout')
		username = self.client.register_login()
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_ban_cannot_join(self):
		channel = random_channel()
		ban_username = random_word()
		ban_password = random_word()
		self.client.register_login(ban_username, ban_password)
		self.client.send(b'logout')
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	self.client.send(b'ban %s %s' % (channel, ban_username))
		self.client.send(b'logout')
		self.client.send(b'login %s %s' % (ban_username, ban_password))
	 	result = self.client.send(b'join %s' % channel)
		self.assertEqual(self.client.reply('CHANNEL_BANNED',{ 'name':channel }), result)

	def test_ban_cannot_follow(self):
		channel = random_channel()
		ban_username = random_word()
		ban_password = random_word()
		self.client.register_login(ban_username, ban_password)
		self.client.send(b'logout')
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	self.client.send(b'ban %s %s' % (channel, ban_username))
		self.client.send(b'logout')
		self.client.send(b'login %s %s' % (ban_username, ban_password))
	 	result = self.client.send(b'follow %s' % channel)
		self.assertEqual(self.client.reply('CHANNEL_BANNED',{ 'name':channel }), result)

	def test_ban_add_no_channel(self):
		ban_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('CHANNEL_NOT_EXIST',{ 'name':channel }), result)

	def test_ban_add_exists(self):
		ban_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('CHANNEL_BANNED_ALREADY',{ 'name':channel, "username":ban_username }), result)

	def test_ban_add_not_admin(self):
		channel = random_channel()
		banned_username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
		result = self.client.send(b'logout')
		username = self.client.register_login()
	 	result = self.client.send(b'ban %s %s' % (channel, banned_username))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_unban(self):
		ban_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	result = self.client.send(b'unban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('CHANNEL_UNBAN',{ 'name':channel, "username":ban_username }), result)

	def test_ban_not_admin(self):
		channel = random_channel()
		ban_username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
		result = self.client.send(b'logout')
		username = self.client.register_login()
	 	result = self.client.send(b'ban %s %s' % (channel, ban_username))
	 	result = self.client.send(b'unban %s %s' % (channel, ban_username))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_unban_join(self):
		ban_username = random_word()
		ban_password = random_word()
		self.client.register_login(ban_username, ban_password)
		self.client.send(b'logout')

		channel = random_channel()
		self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	self.client.send(b'ban %s %s' % (channel, ban_username))
	 	self.client.send(b'unban %s %s' % (channel, ban_username))
		self.client.send(b'logout')
	 	self.client.send(b'login %s %s' % (ban_username, ban_password))
	 	result = self.client.send(b'join %s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_JOIN',{ 'name':channel }), result)





if __name__ == '__main__':
  unittest.main()