from mongokit import Document, Connection
from chat.validators import *
from chat.models.channel import Channel
from chat.models.user import User

import datetime

class Post(Document):
	__collection__ = 'Posts'
	__database__ = 'live'

	structure = {
		'display_name': basestring,
		'sender': User,
		'channel': Channel,
		'recipient': User,
		'format': basestring,
		'data': basestring,
		'likes': int,
		'file': basestring,
		'mentions': [ User ],
		'created': datetime.datetime
	}

	required_fields = ["format","data","display_name"]

	default_values = {
		'likes': 0,
		'format': 'text'
	}

	validators = {
	}

	def post(self, client, user, channel, format, data):
		self['user'] = user
		self['channel'] = channel
		self['format'] = format
		self['data'] = data
		self.save()

		channel.relay(client, 'POST_TEXT_USER', { 'username': user['username'], 'channel': channel['name'], 'text':data })

		return self
