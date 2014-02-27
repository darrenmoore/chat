'''http://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods'''

class Reply(object):
	protocol = 'text'
	@classmethod
	def output(self):
		return self.aaa()


class RplPong(Reply):
	@staticmethod
	def aaa():
		return 'output call'




