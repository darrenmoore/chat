import traceback
import sys
import json
import string, random, uuid
import collections
import re


VERBOSITY_LEVEL = 1


def parse_url(url):
    controller = None
    action = None
    params = {}

    '''Params passed'''
    try:
        param_index = url.index('?')
        param_parts = url[param_index+1:].split('&')
        for part in param_parts:
            kv = part.split('=')
            params[kv[0]] = kv[1]
        url = url[0:param_index]
    except ValueError:
        pass

    '''Controller and action'''
    url = re.sub(r"\/$", '', url)
    url = re.sub(r"^/", '', url)
    url_split = url.split('/')

    controller = url_split[0]
    action = url_split[1]

    return {
        'controller': controller,
        'action': action,
        'params': params
    }  


def print_log(msg):
    if VERBOSITY_LEVEL > 0:
        print '-L- %s' % msg

def print_exc(exc=None, msg=None): 
    if VERBOSITY_LEVEL > 0:
        empty_arg = not exc and not msg
        if empty_arg:
            raise TypeError('print_exc() takes at least one argument (0 given)')
       
        if exc and msg: 
            print '-E- [%s]: %s' % (exc.__class__.__name__, msg)
        elif exc and not msg: 
            print '-E- [%s]: %s' % (exc.__class__.__name__, str(exc))
        else: 
            print '-E- %s' % msg

        if VERBOSITY_LEVEL>=2 and exc:
            traceback.print_exc(file=sys.stderr)
        
def print_warn(msg):
    if VERBOSITY_LEVEL > 0:
        print '-W- %s' % msg
        
def generate_token():
    return str(uuid.uuid4())
        
def random_word(length = 11):
    return ''.join(random.choice(string.lowercase) for i in range(length))
        
def random_channel():
    return '#'+random_word()
        
def random_email():
    return random_word()+'@'+random_word()+'.com'



def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)
