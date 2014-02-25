from mongokit import Document, Connection
from chat.models.user import User
import datetime

class Email(Document):
	__collection__ = 'Emails'
	__database__ = 'live'

	structure = {
		'to_user': User,
		'to_email': basestring,
		'to_name': basestring,
		'from_email': basestring,
		'from_name': basestring,
		'subject': basestring,
		'body': basestring,
		'status': basestring,
		'created': datetime.datetime
	}

	required_fields = []

	default_values = {
		'status': 'pending'
	}