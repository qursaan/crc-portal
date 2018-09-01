#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    # filename='/var/log/fed-service.log',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

import json, urllib2
from flask import Flask, jsonify, abort, request
from flask_crossdomain import crossdomain
# from flaskext.basicauth import BasicAuth
from flaskext.mysql import MySQL

# from paramiko.client import SSHClient
# from paramiko import AutoAddPolicy
# from subprocess import call, Popen
# import threading, os, random, string, portalocker , signal,base64
import time, thread, schedule, threading
# from decorators import *

app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = 'crc-user'
# app.config['BASIC_AUTH_PASSWORD'] = 'crc-pass'
# app.config['BASIC_AUTH_FORCE'] = True
# basic_auth = BasicAuth(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'portal123portal!'
app.config['MYSQL_DATABASE_DB'] = 'PORTAL'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


@app.errorhandler(404)
def resource_not_found(e):
    response = {'message': 'Resource Not Found'}
    response = jsonify(response)
    response.status_code = 404
    return response


@app.errorhandler(401)
def not_authorized(e):
    response = {'message': 'Not Authorized'}
    response = jsonify(response)
    response.status_code = 401
    return response


@app.errorhandler(400)
def not_authorized(e):
    response = {'message': 'Bad Request'}
    response = jsonify(response)
    response.status_code = 400
    return response


@app.errorhandler(405)
def not_authorized(e):
    response = {'message': 'Method Not Allowed'}
    response = jsonify(response)
    response.status_code = 405
    return response


start_flag = False


def start_sync():
    print("Start Sync ...")
    sync_data()
    #schedule.every().minute.do(sync_data)

    """while True:
        schedule.run_pending()
        time.sleep(1)"""

def stop_sync():
    print "Stop Sync ..."
    schedule.clear()


def sync_data():
    global start_flag
    if start_flag:
        try:
            print "Start Sync data"
            conn = mysql.connect()
            cursor = conn.cursor()
            sql_str = """select url from PORTAL.federate_site where id=1;"""
            cursor.execute(sql_str)

            results = cursor.fetchall()

            cursor.close()
            conn.close()

            if results:
                try:
                    server_ip = results[0][0]
                    print "Server IP" , server_ip

                    result = urllib2.urlopen(server_ip + 'federation/fed/update/')
                    if result.getcode() == 200:
                        print "Success"
                    else:
                        print "Fail"
                except Exception as ins :
                    print "ERROR CONNECT TO SITE ", ins.message

        except Exception as ins:
            print "ERROR: ", ins.message

    print "End Sync data"


@app.route('/')
def hello_world():
    return 'CRC Federation Started!'


@app.route('/api/v1/fed/status/', methods=['GET'])
@crossdomain(origin='*')
def api_fed_status():
    global start_flag
    if start_flag:
        return jsonify({'status': 'on'})
    else:
        return jsonify({'status': 'off'})


@app.route('/api/v1/fed/start/', methods=['GET'])
@crossdomain(origin='*')
def api_fed_start():
    global start_flag
    start_flag = 1
    if start_flag:
        start_sync()
        return jsonify({'status': 'on'})
    else:
        return jsonify({'status': 'off'})


@app.route('/api/v1/fed/stop/', methods=['GET'])
@crossdomain(origin='*')
def api_fed_stop():
    global start_flag
    start_flag = 0
    if start_flag:
        return jsonify({'status': 'on'})
    else:
        stop_sync()
        return jsonify({'status': 'off'})


@app.route('/api/v1/fed/valid/key/', methods=['POST'])
@crossdomain(origin='*')
def api_fed_valid_key():
    json_req = request.get_json(force=True, silent=True)

    if json_req == None or 'pkey' not in json_req:
        return abort(400)

    try:
        pkey = json_req['pkey']
        # print "Pkey: ", pkey

        conn = mysql.connect()
        cursor = conn.cursor()
        sql_str = """select public_key, private_key from PORTAL.federate_site where id=1;"""
        cursor.execute(sql_str)

        results = cursor.fetchall()

        cursor.close()
        conn.close()
        # print "RESULTS " , results.count()

        if results:
            try:
                from Crypto.PublicKey import RSA

                newkey = RSA.importKey(json.loads(pkey))
                enc_data = newkey.encrypt("1234567", 32)
                # print enc_data
                pkey = RSA.importKey(json.loads(results[0][1]))
                dec_data = pkey.decrypt(enc_data)
                # print dec_data
            except Exception as ins:
                print "ERROR: ", ins.message

            if dec_data == "1234567":
                print 'ok'
                return jsonify({'status': 'ok'})
            else:
                return jsonify({'status': 'false'})
    except:
        return jsonify({'status': 'false'})
    return jsonify({'status': 'false'})


def start_logo():
    print '''
       __________  ______   ______         __                __  _           
      / ____/ __ \/ ____/  / ____/__  ____/ /__  _________ _/ /_(_)___  ____
     / /   / /_/ / /      / /_  / _ \/ __  / _ \/ ___/ __ `/ __/ / __ \/ __ \ 
    / /___/ _, _/ /___   / __/ /  __/ /_/ /  __/ /  / /_/ / /_/ / /_/ / / / /
    \____/_/ |_|\____/  /_/    \___/\__,_/\___/_/   \__,_/\__/_/\____/_/ /_/
                                              CRC Federation Backend Service
    '''


if __name__ == '__main__':
    start_logo()

    app.run(
        host='0.0.0.0',
        port=7770,
        debug=True,
        use_reloader=False,
        threaded=True)
