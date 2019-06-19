__author__ = 'pirate'

import base64
import json
import urllib
from crc.settings import BACKENDIP, BACKEND_RUN

# USER_HOME = "/home/crc-users/"

BACKEND_IP = BACKENDIP #"193.227.16.199"


# User Management ####################################################
def create_backend_user(username, password):
    if not BACKEND_RUN:
        return 1
    post_data = {
        "username": username,
        "password": password
    }
    post_data = json.dumps(post_data)
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/user/')
    with urllib.request.urlopen(req, data=data) as f:
        result = f.read()
        if result.getcode() == 200:
            return 1
    return 0


# Virtual Machine ####################################################
def get_vm_status(vm_name):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/status')
    with urllib.request.urlopen(req) as f:
        content = f.read()
        return content
    return None


def vm_start(vm_name):
    data = urllib.parse.urlencode('').encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/start')
    with urllib.request.urlopen(req, data=data) as f:
        result = f.read()
        if result.getcode() == 200:
            return 1
    return 0


def vm_restart(vm_name):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/reset')
    with urllib.request.urlopen(req) as f:
        result = f.read()
        if result.getcode() == 200:
            return 1
    return 0


def vm_shutdown(vm_name):
    data = urllib.parse.urlencode('').encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/stop')
    with urllib.request.urlopen(req, data=data) as f:
        result = f.read()
        if result.getcode() == 200:
            return 1
    return 0


# Slicing ############################################################
def create_slice(username, start_time, end_time, node_list):
    # TODO: Remove and update backend services to pass user ontime
    if not BACKEND_RUN :
        return 1
    post_data = {
        'username': username,
        'nodes_list': node_list,
        'start_time': str(start_time.strftime('%H:%M %Y-%m-%d')),
        'end_time': str(end_time.strftime('%H:%M %Y-%m-%d')),
    }
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/slice/')
    with urllib.request.urlopen(req, data=data) as f:
        result = f.read()
        if result.getcode() == 200:
            return 1
    return 0


# Imaging ############################################################
def load_images(task_id, img_name, img_path, node_list):
    post_data = {
        "task_id": task_id,
        "name": img_name,
        "path": img_path,
        "nodes_list": node_list
    }
    post_data = json.dumps(post_data)
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/image/load')
    with urllib.request.urlopen(req, data=data) as f:
        if f.getcode() == 200:
            result = f.read()
            return 1
    return 0


def save_images(task_id, img_name, img_path, node_list):
    post_data = {
        "task_id": str(task_id),
        "name": img_name,
        "path": img_path,
        "nodes_list": [node_list]
    }
    post_data = json.dumps(post_data)
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/image/save')
    with urllib.request.urlopen(req, data=data) as f:
        if f.getcode() == 200:
            result = f.read()
            return 1
    return 0


def check_load_images(task_id):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/image/load/' + str(task_id))
    with urllib.request.urlopen(req) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


def check_save_images(task_id):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/image/save/' + str(task_id))
    with urllib.request.urlopen(req) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


# Experiments ############################################################
def exe_script(script, username):
    post_data = {
        "username": username,
        "script": base64.b64encode(script)
    }
    post_data = json.dumps(post_data)
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/experiment/')
    with urllib.request.urlopen(req, data=data) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


def exe_check(exp_id):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/experiment/' + str(exp_id))
    with urllib.request.urlopen(req) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


def exe_abort(exp_id):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/experiment/' + str(exp_id))
    req.get_method = lambda: 'DELETE'  # or 'DELETE'
    with urllib.request.urlopen(req) as f:
        if f.getcode() == 200:
            return 1
    return 0


# Experiments Lab ############################################################
def commlab_exe(post_data):
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/commlabs/')
    with urllib.request.urlopen(req, data=data) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


def commlab_check(user_id):
    req = urllib.request.Request('http://'+BACKEND_IP+':7777/api/v1/commlabs/status/' + str(user_id))
    with urllib.request.urlopen(req) as f:
        if f.getcode() == 200:
            result = f.read()
            return result
    return 0


def commlab_result(user_id):
    return 'http://'+BACKEND_IP+':7777/api/v1/commlabs/results/' + str(user_id)
    #result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/commlabs/results/' + str(user_id))
    #if result.getcode() == 200:
    #    return result.read()
    #else:
    #    return 0'''

