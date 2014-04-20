from chat.controllers.app_controller import AppController
from chat.validators import *

from chat.models.channel import Channel
from chat.models.post import Post


class PostsController(AppController):

	def add(self, channel, data, sender_ident = None, type = "text"):
		if self.request.logged_in() == False:
			return 'NOT_LOGGED_IN'

		channel = self.db.Channel.find_one({ 'name':channel })
		user = self.request.user()

		recipients = [ channel ]

		post = self.db.Post.post(client=self.request, user=user, recipients=recipients, data=data)
		
		return { "code":'POST_RECEIVED', "data":post }
