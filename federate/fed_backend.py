__author__ = 'pirate'

import base64
import json
import urllib2
from crc.settings import BACKENDIP

USER_HOME = "/home/crc-users/"
BACKEND_IP = BACKENDIP #"193.227.16.199"


def fed_status():
    result = urllib2.urlopen('http://' + BACKEND_IP + ':7770/api/v1/fed/status/')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def fed_start():
    result = urllib2.urlopen('http://' + BACKEND_IP + ':7770/api/v1/fed/start/')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def fed_stop():
    result = urllib2.urlopen('http://' + BACKEND_IP + ':7770/api/v1/fed/stop/')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def validate_key(site,pkey):
    post_data = {
        "pkey": pkey
    }
    post_data = json.dumps(post_data)
    try:
        result = urllib2.urlopen(site+'api/v1/fed/valid/key/', data=post_data)
    except Exception as ee:
        return 2
    if result.getcode() == 200:
        data = result.read()
        if "ok" in data:
            return 1
    return 0