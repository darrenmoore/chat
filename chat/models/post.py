from mongokit import Document, Connection
from chat.validators import *
from chat.models.channel import Channel
from chat.models.user import User
from chat.utils import *

import datetime

class Post(Document):
	__collection__ = 'Posts'
	__database__ = 'live'

	structure = {
		'_id': basestring,							#Guid for this post
		'display_name': basestring,			#By default the users username but can be changed
		'sender_ident': basestring,			#If an ident has been passed this will be send back
		'sender': User,
		'recipients': list,
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

	def post(self, client, user, recipients, data, format = 'text', sender_ident = None):
		self['_id'] = generate_token()
		if sender_ident is None:
			self['sender_ident'] = self['_id']

		self['sender'] = user
		self['recipients'] = recipients
		self['format'] = format
		self['data'] = data
		self['display_name'] = user['username']
		self.save()

		channel = recipients[0]

		for recipient in recipients:
			recipient.relay(client, 'POST_TEXT_USER', { 'username': user['username'], 'channel': channel['name'], 'text':data })
			
		return self
