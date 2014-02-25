import thread
import time

from mongokit import Document, Connection

from controllers.users_controller import UsersController
from controllers.channels_controller import ChannelsController
from controllers.posts_controller import PostsController
from controllers.systems_controller import SystemsController

from models.user import User
from models.channel import Channel
from models.post import Post
from models.email import Email

from protocols.text_protocol import TextProtocol
from protocols.json_protocol import JsonProtocol

from server import Server
from session import Session
from emailer import Emailer


class Chat():

	def __init__(self):
		self.sessions = {}
		return

	def init(self):
		print('Chat started')

		#Database connection
		self.database()

		#Setup
		self.protocols()
		self.email()
		self.controllers()

		#Server
		self.server()

	#Protocols
	def protocols(self):
		print('Loading Protocols')
		self.JsonProtocol = JsonProtocol()
		self.TextProtocol = TextProtocol()

	#Database connection
	def database(self):
		print('Loading Database')
		self.connection = Connection()
		self.connection.register([User])
		self.connection.register([Channel])
		self.connection.register([Post])
		self.connection.register([Email])

	def email(self):
		print('Loading Email')
		self.Emailer = Emailer(self.connection)

	def controllers(self):
		print('Loading Controllers')
		self.UsersController = UsersController(self)
		self.ChannelsController = ChannelsController(self)
		self.PostsController = PostsController(self)
		self.SystemsController = SystemsController(self)

	#Server connection
	def server(self):
		print('Loading Server')
		self.srv = Server()
		self.srv.start(self)
