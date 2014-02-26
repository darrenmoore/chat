import chat.protocols.replies as Replies
from chat.utils import *


class TextProtocol(object):

  def process(self, client, code, data):
    reply = getattr(Replies, code)

    if 'method' in reply:
        output = reply['method'](data)
    else:
        output = reply['message']
        output = output % data

        # if data:
        #     data = flatten(data)
        #     output = output.format(**data)

    if type(output) is list:
        for i in output:
            client.sendLine(str(i))                
        return

    client.sendLine(str(output))