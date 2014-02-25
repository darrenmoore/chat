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

    def start(self, Chat):
        self.connections_count = 0
        self.users = {}
        self.host = '127.0.0.1'
        self.port = 2020
        self.Chat = Chat
        self._listen(2020,'telnet');
        self._listen(8080,'http');
        reactor.run()

    def _listen(self, port, protocol):
        print('Starting to listen on port %s' % port)
        reactor.listenTCP(port, Server(self.Chat, protocol))

    def buildProtocol(self, addr):
        if self.protocol == 'telnet':
            return TelnetClient(self.Chat)
        else:
            return HttpClient(self.Chat)
