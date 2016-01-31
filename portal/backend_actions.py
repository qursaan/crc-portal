__author__ = 'pirate'

import urllib2
import json

USER_HOME = "/home/crc-users/"


# User Management ##########################
def create_backend_user(username, password):
    post_data = {
        "username": username,
        "password": password
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/user/', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


# Virtual Machine ##########################
def get_vm_status(vm_name):
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/vm/'+vm_name+'/status')
    content = result.read()
    return content


def vm_start(vm_name):
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/vm/'+vm_name+'/start', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def vm_restart(vm_name):
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/vm/'+vm_name+'/reset', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


def vm_shutdown(vm_name):
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/vm/'+vm_name+'/stop', data='')
    if result.getcode() == 200:
        return 1
    else:
        return 0


# Imaging ##########################
def load_images(task_id, img_name,img_path,node_list):
    post_data = {
        "task_id": task_id,
        "name": img_name,
        "path": img_path,
        "nodes_list": node_list
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/image/load', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


def save_images(img_name,img_path,node_list):
    post_data = {
        "name": img_name,
        "path": img_path,
        "nodes_list": node_list
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/image/save', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0


# Experiments
def exe_script(path):
    post_data = {
        "path": path
    }
    post_data = json.dumps(post_data)
    result = urllib2.urlopen('http://193.227.16.154:7777/api/v1/experiment/', data=post_data)
    if result.getcode() == 200:
        return 1
    else:
        return 0
