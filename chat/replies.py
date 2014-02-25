
def channel_list(data):
	out = []
	for channel in data:
		out.append('%s' % channel['name'])
	return out

def user_list(channel):
	out = []
	print channel['joined']
	for user in channel['joined']:
		out.append('%s' % user['username'])
	return out

def sessions_list(data):
	out = []
	for sid in data['sessions']:
		out.append('%s' % sid)
	return out

def post_text(post):
	return '(%s) %s: %s' % (post['channel']['name'], post['user']['username'], post['data'])


PONG = {
	'message': "PONG"
}

WELCOME = {
	'message': "Welcome"
}


ERR_UNKNOWN = {
	'message': "Unknown error occurred",
	'success': False,
	'header': '500'
}

ERR_UNKNOWN_COMMAND = {
	'message': "Unknown command",
	'success': False,
	'header': '404'
}

ERR_NOT_LOGGED_IN = {
	'message': 'Not logged in',
	'success': False,
	'header': '401'
}

ERR_ALREADY_LOGGED_IN = {
	'message': "Already logged in",
	'success': False,
	'header': '405'
}

ERR_USER_INVALID_TOKEN = {
	'message': "Invalid user token",
	'success': False,
	'header': '401'
}

ERR_UNKNOWN = {
	'message': "Unknown error occurred",
	'success': False,
	'header': '500'
}
NOT_LOGGED_IN = {
	'message': "Not logged in",
	'success': False,
	'header': '401'
}


USER_REGISTER = {
	'message': "Registered",
	'header': '201'
}

USER_FORGOTTEN = {
	'message': "Reset instructions sent to %(email)s"
}

USER_RESET = {
	'message': "Password for %(username)s has been updated"
}

USER_RESET_TOKEN_NOT_FOUND = {
	'message': "Reset token not found",
	'success': False
}

USER_LOGOUT = {
	'message': "Logged out"
}

USER_LOGIN = {
	'message': "Logged in"
}

USER_USERNAME_ALREADY_TAKEN = {
	'message': "Username taken",
	'success': False
}

USER_USERNAME_NOT_FOUND = {
	'message': "Username not found",
	'success': False
}

USER_PASSWORD_INVALID = {
	'message': "Invalid password",
	'success': False
}

USER_STATUS = {
	'message': "Your status is now '%(status)s'"
}

USER_STATUS_INVALID = {
	'message': "Invalid status '%(status)s'"
}

USER_SET = {
	'message': "Set %(field)s to \"%(value)s\""
}

USER_PROTOCOL = {
	'message': "Protocol changed"
}

USER_PROTOCOL_NOT_FOUND = {
	'message': "Protocol not found"
}

USER_JOINED = {
	'message': channel_list
}

USER_JOINED_NONE = {
	'message': 'No channels joined'
}

USER_FOLLOWING = {
	'method': channel_list
}

USER_INFO = {
	'message': "%(value)s"
}

USER_SESSION = {
	'message': "%(sid)s",
	'data': [
		'sid'
	]
}

USER_SESSIONS_ALL = {
	'method': sessions_list
}

USER_TOKEN = {
	'message': "%(token)s"
}

USER_WHOAMI = {
	'message': "%(username)s"
}

USER_FOLLOWING_NONE = {
	'message': 'No channels followed'
}


CHANNEL_CREATE = {
	'message': "Created %(name)s"
}

CHANNEL_INFO = {
	'message': "Channel information for %(name)s",
	'data': [
		'name'
	]
}

CHANNEL_LIST = {
	'method': channel_list,
	'data_type': 'list',
	'data': [
		'name'
	]
}

CHANNEL_INVALID_NAME = {
	'message': "Invalid channel name",
	'success': False
}

CHANNEL_ALREADY_EXISTS = {
	'message': "Channel already exists",
	'success': False
}

CHANNEL_NO_SUCH_CHANNEL = {
	'message': "Channel does not exist",
	'success': False
}

CHANNEL_USER_JOINED = {
	'message': "%(username)s has joined %(channel)s"
}

CHANNEL_USER_PARTED = {
	'message': "%(username)s has parted %(channel)s"
}

CHANNEL_JOIN = {
	'message': "Joined %(name)s"
}

CHANNEL_PART = {
	'message': "Parted %(name)s"
}

CHANNEL_PART_NOT_JOINED = {
	'message': "Not joined %(name)s"
}

CHANNEL_USER_LIST = {
	'method': user_list
}

CHANNEL_NOT_EXIST = {
	'message': "Channel %(name)s does not exist"
}

CHANNEL_JOINED_ALREADY = {
	'message': "Already joined %(name)s"
}

CHANNEL_FOLLOW = {
	'message': "Following %(name)s"
}

CHANNEL_FOLLOWING_ALREADY = {
	'message': "Already following %(name)s"
}

CHANNEL_UNFOLLOW = {
	'message': "Unfollow %(name)s"
}

CHANNEL_UNFOLLOW_NOT_FOLLOWING = {
	'message': "Not following %(name)s"
}


POST_TEXT = {
	'method': post_text
}

POST_TEXT_USER = {
	'message': "(%(channel)s) %(username)s: %(text)s"
}





