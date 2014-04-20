from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from chat.session import Session
from chat.utils import *


class AppClient(LineReceiver):

    def __init__(self, Chat):
        self.Chat = Chat
        self._protocol = 'text'
        self._user = None

        self.Session = Session(self)
        self.Chat.sessions[self.Session.sid()] = self.Session

        self.startup()

    def connectionMade(self):
        print "New connection (%s)" % self.Session.sid()
        #self.send('WELCOME')

    def connectionLost(self, reason):
        if self.Session.sid():
            self.Session.remove()
        print 'Connection lost (%s)' % self.Session.sid()

    def set_protocol(self, type):
        self._protocol = type

    def get_protocol(self):
        return self._protocol

    def close(self):
        if self.transport.connected:
            self.transport.loseConnection()

    def relay(self, sessions = None, code = None, *args):
        if sessions is None:
            sessions = []
            for sid in self.Chat.sessions:
                sessions.append(sid)

        for sid in sessions:
            if self.Chat.sessions[sid]:
                self.Chat.sessions[sid].client.send(code, *args)

    def send(self, code, data = None):
        protocol = self.get_protocol()
        if protocol == 'text':
            result = self.Chat.TextProtocol.process(self, code, data)
        elif protocol == 'json':
            result = self.Chat.JsonProtocol.process(self, code, data)

    def user_login(self, username, password):
        user = self.Chat.connection.User.find_one({ 'username':username })
        if user is None:
            return 'USER_USERNAME_NOT_FOUND'
        if user['password'] != password:
            return 'USER_PASSWORD_INVALID'
        user.login(self)
        return 'USER_LOGIN'

    def set_user(self, user):
        self.Session.user(user)
        self._user = user

    def user(self):
        return self.Session.get_user()

    def logged_in(self):
        if(self._user):
            return True
        return False

    def dispatch(self, controller, method, args):
        controller = getattr(self.Chat, controller)
        controller.set_requester(self)
        controller.set_method(method)

        if controller.before_filter():
            result = getattr(controller, method)(**args)
            controller.after_filter()
        else:
            result = controller.get_error()

        if result == False:
            result = 'ERR_UNKNOWN_COMMAND'

        if result:
            if 'code' not in result:
                result = { 'code':result, 'data':{} }
            self.send(result['code'], result['data'])