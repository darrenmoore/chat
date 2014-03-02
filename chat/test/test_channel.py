import sys, os
import unittest
import socket
from chat.utils import *

sys.path.insert(0, os.path.dirname(__file__))

from chat.test.client import Client

class TestChannel(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def test_create(self):
		username = self.client.register_login()
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual('Created %s' % channel, result)

	def test_create_invalid(self):
		username = self.client.register_login()
		channel = random_word()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_INVALID_NAME'), result)

	def test_create_already_exists(self):
		username = self.client.register_login()
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('CHANNEL_ALREADY_EXISTS'), result)

	def test_create_not_logged_in(self):
		channel = random_channel()
	 	result = self.client.send(b'create %s' % channel)
	 	self.assertEqual(self.client.reply('NOT_LOGGED_IN'), result)

	def test_list(self):
		username = self.client.register_login()
	 	result = self.client.send(b'list')
	 	self.assertNotEqual(result,'None')

	def test_join(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_JOIN',{ "name":name }), result)

	def test_part(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'part %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_PART',{ "name":name }), result)

	def test_part_not_joined(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'part %s' % name)
	 	result = self.client.send(b'joined')
	 	self.assertEqual(self.client.reply('USER_JOINED_NONE'), result)

	def test_join_not_exist(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_NOT_EXIST', { "name":name }), result)

	def test_joined_already(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_JOINED_ALREADY',{"name":name}), result)

	def test_follow(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_FOLLOW',{"name":name}), result)

	def test_following_already(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_FOLLOWING_ALREADY',{"name":name}), result)

	def test_unfollow(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'follow %s' % name)
	 	result = self.client.send(b'unfollow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW',{"name":name}), result)

	def test_unfollow_not_following(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'unfollow %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW_NOT_FOLLOWING',{ "name":name }), result)

	def test_joined_already(self):
		username = self.client.register_login()
		name = random_channel()
	 	result = self.client.send(b'create %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	result = self.client.send(b'join %s' % name)
	 	self.assertEqual(self.client.reply('CHANNEL_JOINED_ALREADY',{ "name":name }), result)

	def test_invite(self):
		username = self.client.register_login()
	 	result = self.client.send(b'logout')
		channel = random_channel()
		self.client.register_login()
	 	result = self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'join %s' % channel)
	 	result = self.client.send(b'invite %s %s' % (channel, username))
	 	self.assertEqual(self.client.reply('CHANNEL_INVITE',{ "username": username, "name":channel }), result)

	def test_invite_channel_not_exist(self):
		username = self.client.register_login()
	 	result = self.client.send(b'logout')
		channel = random_channel()
		self.client.register_login()
	 	result = self.client.send(b'invite %s %s' % (channel, username))
	 	self.assertEqual(self.client.reply('CHANNEL_NOT_EXIST',{ "name":channel }), result)

	def test_invite_username_not_exist(self):
		username = random_word()
		channel = random_channel()
		self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'invite %s %s' % (channel, username))
	 	self.assertEqual(self.client.reply('USER_NOT_EXIST',{ "username":username }), result)

	def test_admins_list(self):
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'admins %s' % channel)
	 	self.assertTrue(username in result)

	def test_admins_add(self):
		admin_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('CHANNEL_ADMINS_ADD',{ 'name':channel, "username":admin_username }), result)

	def test_admins_add_no_channel(self):
		admin_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('CHANNEL_NOT_EXIST',{ 'name':channel }), result)

	def test_admins_add_exists(self):
		admin_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('CHANNEL_ADMINS_ALREADY',{ 'name':channel, "username":admin_username }), result)

	def test_admins_add_not_admin(self):
		channel = random_channel()
		admin_username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
		result = self.client.send(b'logout')
		username = self.client.register_login()
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_admins_remove(self):
		admin_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'admin_add %s %s' % (channel, admin_username))
	 	result = self.client.send(b'admin_remove %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('CHANNEL_ADMINS_REMOVE',{ 'name':channel, "username":admin_username }), result)

	def test_admins_remove_not_admin(self):
		channel = random_channel()
		admin_username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
		result = self.client.send(b'logout')
		username = self.client.register_login()
	 	result = self.client.send(b'admin_remove %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('NO_PERMISSION'), result)

	def test_admins_remove_user_not_added(self):
		admin_username = self.client.register_login()
		result = self.client.send(b'logout')
		channel = random_channel()
		username = self.client.register_login()
	 	self.client.send(b'create %s' % channel)
	 	result = self.client.send(b'admin_remove %s %s' % (channel, admin_username))
	 	self.assertEqual(self.client.reply('CHANNEL_ADMINS_NOT_ADDED',{ 'name':channel, "username":admin_username }), result)

	# def test_users(self):
	# 	name = random_channel()
	#  	result = self.client.send(b'create %s' % name)
	#  	result = self.client.send(b'join %s' % name)
	#  	result = self.client.send(b'users %s' % name)
	#  	self.assertEqual(self.client.reply('CHANNEL_UNFOLLOW_NOT_FOLLOWING',{ "name":name }), result)



if __name__ == '__main__':
  unittest.main()