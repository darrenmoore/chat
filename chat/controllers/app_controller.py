
class AppController():

	request = None

	def __init__(self, Chat):
		self.db = Chat.connection
		self.emailer = Chat.Emailer
		return

	def requester(self,request):
		self.request = request

	def validate(self, model, field, value):
		return True
		#Validation model method
		method = 'validate_'+field;
		getattr(model, method)()

		print 'Validate: '+value
		return
		
