from mongokit import Document, Connection
from chat.validators import *
from chat.models.user import User
from chat.utils import *

import datetime


class Channel(Document):
	__collection__ = 'Channels'
	__database__ = 'live'

	clients = list

	structure = {
		'name': basestring,						#Name of channel
		'profile': {
			'title': basestring,
			'description': basestring,
			'url': basestring,
			'facebook': basestring,
			'twitter': basestring,
			'instagram': basestring
		},
		'modes': {
			'private': bool,
			'moderated': bool,
			'registered_only': bool
		},
		'token': basestring,
		'creator': User,							#Who created the channel
		'admins': list,								#Admins
		'joined': list,								#Users in channel currently
		'following': list,						#Users who are following the channel
		'activity': list,							#All chat history for this channel
		'created': datetime.datetime
	}

	required_fields = ["name"]

	default_values = {
		'modes': {
			'private': False,							#Cannot be searched for, requires invite
			'moderated': False,						#Only admins can post
			'registered_only': True				#Only registered users can post
		}
	}

	indexes = [
		{
			'fields': [ 'name' ],
			'unique': True
		}
	]

	validators = {
	 	'name': channel_name_validator
	}

	def create(self, name, user):
		self['name'] = name
		self['creator'] = user
		self['admins'] = [ user ]
		self['token'] = generate_token()
		self.save()

	def relay(self, client, line, data):
		sessions = []
		for user in self['joined']:									#users joined channel
			for sid in user['sessions']:							#user sessions
				if sid is not client.Session.sid():			#make sure not the same session as the sender
					sessions.append(sid)

		client.relay(sessions, line, data)

	def already_joined(self, user, name):
		for channel in user['joined']:
			if str(channel['name']) == name:
				return True
		return False

	def already_following(self, user, name):
		for channel in user['following']:
			if str(channel['name']) == name:
				return True
		return False

	def join(self, user, client):
		self.collection.update(
			{ "_id": self["_id"] }, 
			{	"$push": { "joined":user } }
		);
		self.reload()
		self.relay(client, 'CHANNEL_USER_JOINED', { 'username': user['username'], 'channel': self['name'] })
		return True

	def part(self, user, client):
		name = self['name']
		index = 0
		for channel in user['joined']:
			if str(channel['name']) == name:
				del user['joined'][index]
				return True
			index += 1
		self.relay(client, 'CHANNEL_USER_PARTED', { 'username': user['username'], 'channel': self['name'] })
		return False

	def unfollow(self, user, name):
		index = 0
		for channel in user['following']:
			if str(channel['name']) == name:
				del user['following'][index]
				return True
			index += 1
		return False
