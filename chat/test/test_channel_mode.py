import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client

class TestChannelMode(unittest.TestCase):

	def setUp(self):
		self.modes = ['private','moderated','registered_only']
		self.client = Client()

	def tearDown(self):
		self.client.connection.close()

	def test_set_anonymous(self):
		result = self.mode_on('anonymous','on')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'anonymous', 'mode_value':True }), result)

	def test_set_anonymous_ff(self):
		result = self.mode_on('anonymous','off')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'anonymous', 'mode_value':False }), result)

	def test_set_private(self):
		result = self.mode_on('private','on')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'private', 'mode_value':True }), result)

	def test_set_private_ff(self):
		result = self.mode_on('private','off')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'private', 'mode_value':False }), result)

	def test_set_moderated(self):
		result = self.mode_on('moderated','on')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'moderated', 'mode_value':True }), result)

	def test_set_moderated_off(self):
		result = self.mode_on('moderated','off')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'moderated', 'mode_value':False }), result)

	def test_set_registered_only(self):
		result = self.mode_on('registered_only','on')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'registered_only', 'mode_value':True }), result)

	def test_set_registered_only_off(self):
		result = self.mode_on('registered_only','off')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_SET',{ 'field':'registered_only', 'mode_value':False }), result)

	def test_set_invalid_mode(self):
		result = self.mode_on('foobar','on')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_NOT_FOUND',{ 'field':'foobar' }), result)

	def test_set_invalid_value(self):
		result = self.mode_on('private','foobar')
	 	self.assertEqual(self.client.reply('CHANNEL_MODE_INVALID_VALUE',{ 'value':'foobar' }), result)

	def mode_on(self, mode, switch):
		self.client.register_login()
		channel = random_word()
	 	result = self.client.send(b'create #%s' % channel)
	 	return self.client.send(b'mode #%s %s %s' % (channel, mode, switch))

	def test_set_no_permission(self):
		self.client.register_login()
		channel = random_word()
	 	result = self.client.send(b'create #%s' % channel)
	 	result = self.client.send(b'logout')
		self.client.register_login()
	 	result = self.client.send(b'mode #%s %s %s' % (channel, 'private', 'on'))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_private_join(self):
		'''Make sure cannot join private channel'''
		self.client.register_login()
		channel = random_word()
	 	self.client.send(b'create #%s' % channel)
	 	a = self.client.send(b'mode #%s %s %s' % (channel, 'private', 'on'))
	 	self.client.send(b'logout')
		self.client.register_login()
	 	result = self.client.send(b'join #%s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_PRIVATE', {'name':'#'+channel}), result)

	def test_not_private_join(self):
		self.client.register_login()
		channel = random_word()
	 	self.client.send(b'create #%s' % channel)
	 	self.client.send(b'logout')
		self.client.register_login()
	 	result = self.client.send(b'join #%s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_JOIN', {'name':'#'+channel}), result)

	def test_private_follow(self):
		self.client.register_login()
		channel = random_word()
	 	self.client.send(b'create #%s' % channel)
	 	a = self.client.send(b'mode #%s %s %s' % (channel, 'private', 'on'))
	 	self.client.send(b'logout')
		self.client.register_login()
	 	result = self.client.send(b'follow #%s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_PRIVATE', {'name':'#'+channel}), result)

	def test_not_private_follow(self):
		self.client.register_login()
		channel = random_word()
	 	self.client.send(b'create #%s' % channel)
	 	self.client.send(b'logout')
		self.client.register_login()
	 	result = self.client.send(b'follow #%s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_FOLLOW', {'name':'#'+channel}), result)

	def test_private_invite_join(self):
		channel = random_word()
		invited_username = random_word()
		invited_password = random_word()

		self.client.register_login(invited_username, invited_password)
	 	self.client.send(b'logout')

		b = self.client.register_login()
	 	self.client.send(b'create #%s' % channel)
	 	self.client.send(b'mode #%s %s %s' % (channel, 'private', 'on'))
	 	self.client.send(b'invite #%s %s' % (channel, invited_username))
	 	self.client.send(b'logout')
	 	self.client.send(b'login %s %s' % (invited_username, invited_password))
	 	result = self.client.send(b'join #%s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_JOIN', {'name':'#'+channel}), result)



	# def test_moderated(self):
	# 	'''Cannot post to moderated channel and user is not moderator'''
	# 	pass

	# def test_registered_only(self):
	# 	'''Only registered users can post to channel, no anon posts'''
	# 	pass


if __name__ == '__main__':
  unittest.main()