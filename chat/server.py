from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from clients.telnet_client import TelnetClient
from clients.http_client import HttpClient


class Server(Factory):

    def __init__(self, Chat = False, protocol = 'telnet'):
        self.Chat = Chat
        self.protocol = protocol
        return

    def start(self, Chat, host, port):
        self.connections_count = 0
        self.users = {}
        self.host = host
        self.port = port
        self.Chat = Chat
        self._start();

    def _start(self):
        print('Starting to listen on port %s' % self.port)
        reactor.listenTCP(self.port, Server(self.Chat, 'telnet'))
        reactor.listenTCP(8080, Server(self.Chat, 'http'))
        reactor.run()

    def buildProtocol(self, addr):
        if self.protocol == 'telnet':
            return TelnetClient(self.Chat)
        else:
            return HttpClient(self.Chat)
