import socket
import time

from chat.utils import *
from chat.models.user import User
from chat.models.channel import Channel
from chat.models.post import Post
from chat.models.email import Email

from mongokit import Document, Connection

import chat.protocols.replies as Replies
	

class Client(): 

	def __init__(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect(('localhost',2020))
		#result = self.connection.recv(1024).rstrip()

	def connect_db(self):
		self.db = Connection()
		self.db.register([User])
		self.db.register([Channel])
		self.db.register([Post])
		self.db.register([Email])
		return self.db

	def reply(self, type, data = None):
		reply = getattr(Replies, type)
		message = reply['message']
		if data:
			message = message % data
		return message

	def send(self, msg):
		self.connection.send(msg+"\r\n")
		result = self.connection.recv(1024).rstrip()
		return result

	def register_login(self, username = None, password = None):
		if username is None:
			username = random_word()

		if password is None:
			password = random_word()
			
		email = random_email()

		result = self.send(b'register %s %s %s' % (username, password, email))
		#result = self.send(b'login %s %s' % (username, password))
		return username

	def create_channel(self):
		self.register_login()
		channel = random_channel()
	 	result = self.send(b'create %s' % channel)
		return channel

	def tearDown(self):
		self.connection.close()
		self.connection = None