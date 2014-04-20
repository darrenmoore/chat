
class AppController():

	request = None
	method = None

	def __init__(self, Chat):
		self.db = Chat.connection
		self.emailer = Chat.Emailer
		return

	def set_method(self,method):
		self.method = method

	def set_requester(self,request):
		self.request = request

	def before_filter(self):
		return True

	def after_filter(self):
		pass

	def get_error(self):
		pass

	def validate(self, model, field, value):
		return True
		#Validation model method
		method = 'validate_'+field;
		getattr(model, method)()

		print 'Validate: '+value
		return
		
