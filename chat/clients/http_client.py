from chat.clients.app_client import AppClient
from chat.utils import *


class HttpClient(AppClient):

    def startup(self):
        self.set_protocol('json')
        self.headers = {}
        self.type = 'GET'
        self.url = None

    def lineReceived(self, line):
        if line == "":
            self.route()
            return

        if self.url is None:
            line = line.split(' ')
            self.type = line[0]
            self.url = line[1]
        else:
            line = line.split(': ')
            if len(line) == 2:
                self.headers[line[0]] = line[1]

    def route(self):
        #Route the request
        result = parse_url(self.url)
        self.controller = result['controller']
        self.action = result['action']
        self.params = result['params']

        #Check if they passed a user token
        if self.auth() is False:
            self.send('ERR_USER_INVALID_TOKEN')
            self.close()
            return

        controller = self.controller.title()+'Controller'
        method = self.action
        args = self.params

        self.dispatch(controller, method, args)
        self.close()

    def auth(self):
        token = None

        if 'auth_token' in self.params:
            token = self.params['auth_token']
            del self.params['auth_token']

        if 'Authorization' in self.headers:
            token = self.headers['Authorization']

        if token is None:
            return True

        if self.login(token):
            return True

        return False


    def login(self, token):
        user = self.Chat.connection.User.find_one({ 'token':token })
        if user is None:
            return False
        user.login(self)
        return True
