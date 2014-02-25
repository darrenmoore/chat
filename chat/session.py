from utils import *

class Session(object):

	sessions = {}			#session id, data

	def __init__(self, client):
		self._sid = generate_token()
		self._user = None
		self.client = client

	def sid(self):
		return self._sid

	def user(self, user):
		self._user = user

	def get_user(self):
		return self._user

	def remove(self):
		if self._user is not None:
			self._user.remove_session(self.sid())
