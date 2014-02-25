from chat.controllers.app_controller import AppController

from chat.models.channel import Channel
from chat.models.user import User
from chat.models.post import Post


class SystemsController(AppController):

	def ping(self):
		return 'PONG'
		pass

	def memory(self):
		pass

	def reset(self):
		pass
		# self.db.Channel.remove()
		# self.db.User.remove()
		# self.db.Post.remove()
		# return c.POST_TEXT


	def test(self):
		self.request.relay(None, 'TEST_FORMAT', { 'stringa': 'bbb', 'stringb':'ccc' })