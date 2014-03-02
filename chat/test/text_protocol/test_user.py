import sys, os
import unittest
import socket

sys.path.insert(0, os.path.dirname(__file__))

from chat.utils import *
from chat.test.client import Client
from chat.models.email import Email

class TestUser(unittest.TestCase):

	def setUp(self):
		self.client = Client()
	 	self.client.connect_db()

	def tearDown(self):
		self.client.connection.close()

	def test_whoami_not_logged_in(self):
	 	result = self.client.send(b'whoami')
	 	self.assertEqual(self.client.reply('ERR_NOT_LOGGED_IN'), result)

	def test_whoami(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'whoami')
	 	self.assertEqual(username, result)

	def test_register(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	self.assertEqual(self.client.reply('USER_REGISTER'), result)

	def test_register_already_logged_in(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	self.assertEqual(self.client.reply('ERR_ALREADY_LOGGED_IN'), result)

	def test_register_username_already_taken(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'logout')
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	self.assertEqual(self.client.reply('USER_USERNAME_ALREADY_TAKEN'), result)

	def test_logout(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'logout')
	 	self.assertEqual(self.client.reply('USER_LOGOUT'), result)

	def test_logout_not_logged_in(self):
	 	result = self.client.send(b'logout')
	 	self.assertEqual(self.client.reply('NOT_LOGGED_IN'), result)

	def test_login(self):
		username = random_word()
		email = random_email()
		password = random_word()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'logout')
	 	result = self.client.send(b'login %s %s' % (username, password))
	 	self.assertEqual(self.client.reply('USER_LOGIN'), result)

	def test_login_username_not_found(self):
		username = random_word()
		password = random_word()
	 	result = self.client.send(b'login %s %s' % (username, password))
	 	self.assertEqual(self.client.reply('USER_USERNAME_NOT_FOUND'), result)

	def test_login_password_invalid(self):
		username = random_word()
		password = random_word()
		password_invalid = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'logout')
	 	result = self.client.send(b'login %s %s' % (username, password_invalid))
	 	self.assertEqual(self.client.reply('USER_PASSWORD_INVALID'), result)

	def test_protocol(self):
	 	result = self.client.send(b'protocol text')
	 	self.assertEqual(self.client.reply('USER_PROTOCOL'), result)

	def test_protocol_not_found(self):
	 	result = self.client.send(b'protocol foobar')
	 	self.assertEqual(self.client.reply('USER_PROTOCOL_NOT_FOUND'), result)

	def test_session(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'session')
	 	self.assertNotEqual(result,'None')

	def test_token(self):
		username = random_word()
		password = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'token')
	 	self.assertNotEqual(result,'None')

	def test_set_full(self):
		profile = {
			'name': 'Foo Bar',
			'bio': 'This is my bio',
			'url': 'www.foobar.com',
			'facebook': 'foobar1',
			'twitter': 'foobar2',
			'instagram': 'foobar3'
		}
		username = random_word()
		password = random_word()
		email = random_email()

	 	result = self.client.send(b'register %s %s %s' % (username, password, email))

	 	for key, value in profile.iteritems():
	 		result = self.client.send(b'set %s %s' % (key, value))

	 	pass_count = 0
	 	for key, value in profile.iteritems():
	 		result = self.client.send(b'profile %s' % key)
	 		if result == profile[key]:
	 			pass_count += 1

	 	self.assertNotEqual(pass_count,len(profile))

	def test_following(self):
		self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	result = self.client.send(b'following')
	 	self.assertNotEqual(self.client.reply('USER_FOLLOWING_NONE'),'None')

	def test_following_none(self):
		self.client.register_login()
	 	result = self.client.send(b'following')
	 	self.assertEqual(self.client.reply('USER_FOLLOWING_NONE'), result)

	def test_joined(self):
		self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'joined')
	 	self.assertNotEqual(self.client.reply('USER_JOINED_NONE'),'None')

	def test_joined_none(self):
		self.client.register_login()
	 	result = self.client.send(b'joined')
	 	self.assertEqual(self.client.reply('USER_JOINED_NONE'), result)

	def test_forgotten(self):
		username = random_word()
		password = random_word()
		password_new = random_word()
		email = random_email()
	 	result = self.client.send(b'register %s %s %s' % (username, password, email))
	 	result = self.client.send(b'login %s %s' % (username, password))
	 	result = self.client.send(b'logout')
	 	result = self.client.send(b'forgotten %s' % username)
		user = self.client.db.User.find_one({ 'username':username })
	 	result = self.client.send(b'reset %s %s' % (user['reset_token'], password_new))
	 	result = self.client.send(b'login %s %s' % (username, password_new))
	 	self.assertEqual(self.client.reply('USER_LOGIN'), result)

	def test_status_away(self):
		status = 'away'
		self.client.register_login()
	 	result = self.client.send(b'status %s' % status)
	 	self.assertEqual(self.client.reply('USER_STATUS',{ 'status':status }), result)

	def test_status_offline(self):
		status = 'offline'
		self.client.register_login()
	 	result = self.client.send(b'status %s' % status)
	 	self.assertEqual(self.client.reply('USER_STATUS',{ 'status':status }), result)

	def test_status_dnd(self):
		status = 'dnd'
		self.client.register_login()
	 	result = self.client.send(b'status %s' % status)
	 	self.assertEqual(self.client.reply('USER_STATUS',{ 'status':status }), result)

	def test_status_online(self):
		status = 'online'
		self.client.register_login()
	 	result = self.client.send(b'status %s' % status)
	 	self.assertEqual(self.client.reply('USER_STATUS',{ 'status':status }), result)

	def test_status_invalid(self):
		status = 'foobar'
		self.client.register_login()
	 	result = self.client.send(b'status %s' % status)
	 	self.assertEqual(self.client.reply('USER_STATUS_INVALID',{ 'status':status }), result)

if __name__ == '__main__':
  unittest.main()