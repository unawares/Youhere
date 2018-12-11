import re
import random
import string

REQUEST_FORMAT = {
    'app': str,
    'function': str,
    'args': list,
    'kwargs': dict
}


RESPONSE_FORMAT = {
    'app': str,
    'function': str,
    'result': None
}


def is_valid_request(obj):
    if type(obj) is not dict:
        return False
    if len(obj.keys()) == len(REQUEST_FORMAT.keys()):
        for key in obj:
            if key not in REQUEST_FORMAT:
                return False
            if REQUEST_FORMAT[key] is None:
                continue
            if type(obj[key]) is not REQUEST_FORMAT[key]:
                return False
        return True
    else:
        return False


def is_valid_response(obj):
    if type(obj) is not dict:
        return False
    if set(obj.keys()) == set(RESPONSE_FORMAT.keys()):
        for key in obj:
            if key not in RESPONSE_FORMAT:
                return False
            if RESPONSE_FORMAT[key] is None:
                continue
            if type(obj[key]) is not RESPONSE_FORMAT[key]:
                return False
        return True
    else:
        return False


def generate_key(name, surname):
    key = ''.join(list(filter(str.isalpha, name))).lower() + '.' + ''.join(list(filter(str.isalpha, surname))).lower()
    return key


def generate_random_key(sample=string.ascii_lowercase, width=16):
    return ''.join(random.choices(sample, k=width))
    