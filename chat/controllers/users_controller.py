from chat.controllers.app_controller import AppController
from chat.models.user import User
from chat.utils import *


class UsersController(AppController):

	_before_filter = {

	}

	def login(self, username, password):
		user = self.db.User.find_one({ 'username':username })
		if user is None:
			return 'USER_USERNAME_NOT_FOUND'
		if user['password'] != password:
			return 'USER_PASSWORD_INVALID'
		user.login(self.request)
		return 'USER_LOGIN'

	def logout(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		user = self.db.User()
		user.logout(self.request)
		return 'USER_LOGOUT'

	def register(self, username, password, email):
		if self.request.logged_in() == True:
			return 'ERR_ALREADY_LOGGED_IN'
		if self.db.User.find_one({ 'username':username }):
			return 'USER_USERNAME_ALREADY_TAKEN'
		user = self.db.User()
		user['username'] = username
		user['password'] = password
		user['email'] = email
		user['token'] = generate_token()
		user['validate_email_token'] = generate_token(type='short')
		user.save()
		user.login(self.request);
		self.emailer.send(user['email'], 'Registered!', 'register', user)
		return 'USER_REGISTER'

	def forgotten(self, username):
		if self.request.logged_in() == True:
			return 'ERR_ALREADY_LOGGED_IN'
		user = self.db.User.find_one({ 'username':username })
		if user is None:
			return 'USER_USERNAME_NOT_FOUND'
		user['reset_token'] = generate_token()
		user.save()
		self.emailer.send(user['email'], 'Forgotten password request', 'forgotten', user)
		return { "code":'USER_FORGOTTEN', "data":user }

	def reset(self, reset_token, new_password):
		if self.request.logged_in() == True:
			return 'ERR_ALREADY_LOGGED_IN'
		user = self.db.User.find_one({ 'reset_token':reset_token })
		if user is None:
			return 'USER_RESET_TOKEN_NOT_FOUND'
		user['reset_token'] = None
		user['password'] = new_password
		user.save()
		return { "code":'USER_RESET', "data":user }

	def profile(self, field):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		data = self.request.user()
		value = data["profile"][field]
		return { "code":'USER_INFO', "data":{"value":value} }

	def token(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		data = self.request.user()
		return { "code":'USER_TOKEN', "data":data }

	def set(self, field, value):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		data = self.request.user()
		data["profile"][field] = value
		data.save()
		return { "code":'USER_SET', "data":{"field":field,"value":value} }

	def whoami(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		data = self.request.user()
		return { "code":'USER_WHOAMI', "data":data }

	def quit(self):
		self.request.close()

	def protocol(self, type):
		if type not in ['json','text']:
			return 'USER_PROTOCOL_NOT_FOUND'
		self.request.set_protocol(type)
		return { "code":'USER_PROTOCOL', "data":{"type":type} }

	def joined(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		user = self.request.user()
		channels = user['joined']
		if not channels:
			return { "code":'USER_JOINED_NONE', "data":channels }
		return { "code":'USER_JOINED', "data":channels }

	def following(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		user = self.request.user()
		channels = user['following']
		if not channels:
			return { "code":'USER_FOLLOWING_NONE', "data":channels }
		return { "code":'USER_FOLLOWING', "data":channels }

	def session(self):
		sid = self.request.Session.sid()
		return { "code":'USER_SESSION', "data":{ 'sid':sid, 'test':{'foo':'bar'} } }

	def sessions_all(self):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		user = self.request.user()
		return { "code":'USER_SESSIONS_ALL', "data":user }

	def status(self, value):
		if self.request.logged_in() == False:
			return 'ERR_NOT_LOGGED_IN'
		user = self.request.user()
		if user.status(value):
			return { "code":'USER_STATUS', "data":user }
		else:
			return { "code":'USER_STATUS_INVALID', "data":{ 'status':value } }
			