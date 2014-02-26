import chat.protocols.replies as Replies
import json
from mongokit import Document, Connection, ObjectId
from email.utils import formatdate


class JsonProtocol(object):

  def process(self, client, code, data):
    reply = getattr(Replies, code)

    output = {
        'success': True
    }

    if 'success' in reply:
        output['success'] = reply['success']

    if 'data' in reply:
        data_type = 'dict'

        if 'data_type' in reply:
            data_type = reply['data_type']

        if data_type == 'list':
            output['data'] = []
            for record in data:
                row = {}
                for field in reply['data']:
                    row[field] = record[field]
                output['data'].append(row)
        else:
            output['data'] = {}
            for field in reply['data']:
                output['data'][field] = data[field]

    if 'message' in reply:
        output['message'] = reply['message']
        if data:
            output['message'] = output['message'] % data

        
    #output = json.dumps(output, sort_keys=False)
    output = json.dumps(output, sort_keys=False, cls=JSONEncoder)

    client.sendLine('HTTP/1.1 200 OK')
    client.sendLine('Date: '+formatdate(timeval=None, localtime=False, usegmt=True))
    client.sendLine('Content-Type: application/json')
    client.sendLine('Connection: keep-alive')
    client.sendLine("\r\n")
    client.sendLine("\r\n")
    client.sendLine(str(output))


class JSONEncoder(json.JSONEncoder): 
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, list):
            return json.JSONEncoder.default(self, o)
        else:
            '''Collection'''
            output = []

            for record in o:
                row = {}
                for field in record:
                    if isinstance(field, basestring):
                        row[field] = record[field]
                output.append(row)

            return output