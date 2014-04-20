from chat.controllers.app_controller import AppController
from chat.validators import *

from chat.models.channel import Channel


class ChannelsController(AppController):

	_before_filter = {

	}

	def create(self, name):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		if self.db.Channel.find_one({ 'name':name }):
			return 'CHANNEL_ALREADY_EXISTS'
		if channel_name_validator(name) == False:
			return 'CHANNEL_INVALID_NAME'
		channel = self.db.Channel()
		channel.create(name, self.request.user())
		return { "code":'CHANNEL_CREATE', "data":channel }

	def search(self, keywords):
		channels = self.db.Channel.find_fulltext(keywords)
		print channels

	def info(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
			return 'CHANNEL_NO_SUCH_CHANNEL'
		return { "code":'CHANNEL_INFO', "data":channel }

	def list(self):
		channels = self.db.Channel.find()
		return { "code":'CHANNEL_LIST', "data":channels }

	def join(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_banned(self.request.user()):
			return { "code":'CHANNEL_BANNED', "data":{"name":name} }
		if channel.already_joined(self.request.user(), name):
			return { "code":'CHANNEL_JOINED_ALREADY', "data":{"name":name} }
		code = channel.join(self.request.user(), self.request)
		return { "code":code, "data":channel }

	def part(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if not channel.already_joined(self.request.user(), name):
			return { "code":'CHANNEL_NOT_JOINED', "data":{"name":name} }
		user = self.request.user()
		check = channel.part(self.request.user(), self.request)
		return { "code":'CHANNEL_PART', "data":channel }

	def invite(self, name, username):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		user = self.db.User.find_one({ 'username':username })
		if user is None:
		 	return { "code":'USER_NOT_EXIST', "data":{"username":username} }
		code = channel.invite(user)
		return { "code":code, "data":{'name':channel['name'],'username':user['username']} }

	def mode(self, name, field, value = None):
		if value is not None and self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		user = self.request.user()
		code = channel.mode(user, field, value)
		mode_value = None
		if field in channel['mode']:
			mode_value = channel['mode'][field]

		return { "code":code, "data":{"field":field,"value":value,"mode_value":mode_value} }

	def follow(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_banned(self.request.user()):
			return { "code":'CHANNEL_BANNED', "data":{"name":name} }
		if channel.already_following(self.request.user(), name):
			return { "code":'CHANNEL_FOLLOWING_ALREADY', "data":{"name":name} }
		code = channel.follow(self.request.user(), self.request)
		return { "code":code, "data":channel }

	def unfollow(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if not channel.already_following(self.request.user(), name):
			return { "code":'CHANNEL_UNFOLLOW_NOT_FOLLOWING', "data":{"name":name} }
		user = self.request.user()
		check = channel.unfollow(self.request.user(), name)
		return { "code":'CHANNEL_UNFOLLOW', "data":channel }

	def admins(self, name):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		return { "code":'CHANNEL_ADMINS_LIST', "data":channel }

	def admins_add(self, name, username):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_admin(self.request.user()) == False:
		 	return 'NO_PERMISSION'
		user = self.db.User.find_one({ 'username':username })
		if user is None:
		 	return { "code":'USER_NOT_EXIST', "data":{"username":username} }
		code = channel.admin_add(user)
		return { "code":code, "data":{'name':channel['name'],'username':user['username']} }

	def admins_remove(self, name, username):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_admin(self.request.user()) == False:
		 	return 'NO_PERMISSION'
		user = self.db.User.find_one({ 'username':username })
		if user is None:
		 	return { "code":'USER_NOT_EXIST', "data":{"username":username} }
		code = channel.admin_remove(user)
		return { "code":code, "data":{'name':channel['name'],'username':user['username']} }

	def ban(self, name, username):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_admin(self.request.user()) == False:
		 	return 'NO_PERMISSION'
		user = self.db.User.find_one({ 'username':username })
		if user is None:
		 	return { "code":'USER_NOT_EXIST', "data":{"username":username} }
		code = channel.ban(user)
		return { "code":code, "data":{'name':channel['name'],'username':user['username']} }

	def unban(self, name, username):
		channel = self.db.Channel.find_one({ 'name':name })
		if channel is None:
		 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
		if channel.is_admin(self.request.user()) == False:
		 	return 'NO_PERMISSION'
		user = self.db.User.find_one({ 'username':username })
		if user is None:
		 	return { "code":'USER_NOT_EXIST', "data":{"username":username} }
		code = channel.unban(user)
		return { "code":code, "data":{'name':channel['name'],'username':user['username']} }

	# def joined(self, name):
	# 	channel = self.db.Channel.find_one({ 'name':name })
	# 	if channel is None:
	# 	 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
	# 	if channel['joined'] is None:
	# 	 	return { "code":'CHANNEL_NOT_EXIST', "data":{"name":name} }
	# 	return { "code":'CHANNEL_USER_LIST', "data":channel }
