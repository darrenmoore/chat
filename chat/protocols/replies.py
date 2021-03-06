
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

def admins_list(channel):
	out = []
	print channel['admins']
	for user in channel['admins']:
		out.append('%s' % user['username'])
	return out

def sessions_list(data):
	out = []
	for sid in data['sessions']:
		out.append('%s' % sid)
	return out

def post_text(post):
	return '(%s) %s: %s' % (post['recipients'][0]['name'], post['display_name'], post['data'])


PONG = {
	'message': "PONG"
}

WELCOME = {
	'message': "Welcome"
}


NO_PERMISSION = {
	'message': "No permission",
	'success': False,
	'header': '401'
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

USER_NOT_EXIST = {
	'message': "User %(username)s does not exist",
	'success': False
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

CHANNEL_PRIVATE = {
	'message': '%(name)s is private',
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

CHANNEL_NOT_JOINED = {
	'message': "Not joined %(name)s"
}

CHANNEL_MODE_VALUE = {
	'message': "Channel mode %(field)s is %(mode_value)s"
}

CHANNEL_MODE_SET = {
	'message': "Channel mode %(field)s set to %(mode_value)s"
}

CHANNEL_MODE_NOT_FOUND = {
	'message': "Channel mode %(field)s not found",
	'success': False
}

CHANNEL_MODE_INVALID_VALUE = {
	'message': "Invalid mode value '%(value)s'. Use 'on' or 'off'",
	'success': False
}

CHANNEL_USER_LIST = {
	'method': user_list
}

CHANNEL_INVITE = {
	'message': "%(username)s has been invited %(name)s"
}

CHANNEL_INVITE_ALREADY = {
	'message': "%(username)s has been invited %(name)s already"
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

CHANNEL_ADMINS_LIST = {
	'method': admins_list
}

CHANNEL_ADMINS_ADD = {
	'message': '%(username)s added as an admin to %(name)s'
}

CHANNEL_ADMINS_ALREADY = {
	'message': '%(username)s is already an admin of %(name)s'
}

CHANNEL_ADMINS_REMOVE = {
	'message': '%(username)s removed as an admin to %(name)s'
}

CHANNEL_ADMINS_NOT_ADDED = {
	'message': '%(username)s is not an admin of %(name)s'
}

CHANNEL_BANNED = {
	'message': 'You are banned from %(name)s'
}

CHANNEL_BAN = {
	'message': '%(username)s is banned from %(name)s'
}

CHANNEL_BANNED_ALREADY = {
	'message': '%(username)s is banned already %(name)s'
}

CHANNEL_UNBAN = {
	'message': '%(username)s is unbanned from %(name)s'
}

CHANNEL_UNBAN_NOT_BANNED = {
	'message': '%(username)s is not banned from %(name)s'
}


POST_RECEIVED = {
	'message': 'Received %(sender_ident)s'
}

POST_TEXT = {
	'method': post_text
}

POST_TEXT_USER = {
	'message': "(%(channel)s) %(username)s: %(text)s"
}





