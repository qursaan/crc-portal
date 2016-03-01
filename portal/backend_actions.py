__author__ = 'pirate'

import base64
import json
import urllib2

USER_HOME = "/home/crc-users/"

BACKEND_IP = "193.227.16.199"

# User Management ####################################################
def create_backend_user(username, password):
    post_data = {
        "username": username,
        "password": password
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/user/', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


# Virtual Machine ####################################################
def get_vm_status(vm_name):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/status')
    content = result.read()
    return content


def vm_start(vm_name):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/start', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def vm_restart(vm_name):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/reset', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def vm_shutdown(vm_name):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/vm/' + vm_name + '/stop', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


# Slicing ############################################################
def create_slice(username, start_time, end_time):
    post_data = {
        'user_name': username,
        'start_time': str(start_time),
        'end_time': str(end_time),
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/slice/', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
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
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/image/load', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


def save_images(task_id, img_name, img_path, node_list):
    post_data = {
        "task_id": str(task_id),
        "name": img_name,
        "path": img_path,
        "nodes_list": [node_list]
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/image/save', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


def check_load_images(task_id):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/image/load/' + str(task_id))
    if result.getcode() == 200:
        return result.read()
    else:
        return 0


def check_save_images(task_id):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/image/save/' + str(task_id))
    if result.getcode() == 200:
        return result.read()
    else:
        return 0


# Experiments ############################################################
def exe_script(script, username):
    post_data = {
        "username": username,
        "script": base64.b64encode(script)
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/experiment/', data=post_data)
    if result.getcode() == 200:
        return result.read()
    else:
        return 0


def exe_check(exp_id):
    result = urllib2.urlopen('http://'+BACKEND_IP+':7777/api/v1/experiment/' + str(exp_id))
    if result.getcode() == 200:
        return result.read()
    else:
        return 0


def exe_abort(exp_id):
    request = urllib2.Request('http://'+BACKEND_IP+':7777/api/v1/experiment/' + str(exp_id))
    request.get_method = lambda: 'DELETE'  # or 'DELETE'
    result = urllib2.urlopen(request)
    if result.getcode() == 200:
        return 1
    else:
        return 0

