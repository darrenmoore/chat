from mongokit import Document, Connection
from chat.validators import *
from chat.utils import *

import datetime



class User(Document):
	__collection__ = 'Users'
	__database__ = 'live'

	structure = {
		'username': basestring,
		'password': basestring,
		'email': basestring,
		'token': basestring,
		'reset_token': basestring,
		'validate_email_token': basestring,
		'sessions': list,
		'profile': dict,
		'clients': list,
		'joined': list,
		'following': list,
		'status': basestring,
		'last_activity': datetime.datetime,
		'created': datetime.datetime,
		'modes': dict
	}

	required_fields = []

	default_values = {
		'status': 'offline',
		'profile': {
			'name': None,
			'bio': None,
			'location': None,
			'url': None,
			'facebook': None,
			'twitter': None,
			'instagram': None
		},
		'modes': {
			'away': False,
			'operator': False,
			'invisible': False,
			'klined': False,
			'muted': False,
			'throttled': False,
			'protected': False
		}
	}

	validators = {
		'username': alias_validator,
		'email': email_validator
	}

	indexes = [
		{
			'fields': [ 'username' ],
			'unique': True
		},
		{
			'fields': [ 'email' ]
		}
	]

	statuses = ['online','offline','away','dnd']

	def login(self, client):
		self['sessions'].append(client.Session.sid())
		self.save()
		client.set_user(self)

	def logout(self, client):
		client.set_user(None)

	def remove_session(self, sid = None):
		if sid is None:
			self['sessions'] = []
		else:
			try:
				self['sessions'].remove(sid)
			except ValueError:
				pass
		self.save()

	def status(self, value):
		if value not in self.statuses:
			return False
		self['status'] = value
		self.save()
		return True

	def part_all(self):
		pass
		# joined = self['joined']

		# for channel in self['joined']:
		# 	channel.part(self, )

	def part(self, user, client):
		if sid is None:
			self['sessions'] = []
		else:
			try:
				self['sessions'].remove(sid)
			except ValueError:
				pass
		self.save()