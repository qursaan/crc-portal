from django.core.management.base import BaseCommand, CommandError
import socket
from threading import Thread
from SocketServer import ThreadingMixIn
from howdy.models import output, Values
import sys
import os
import datetime
from portal.models import MyUser, PhysicalNode
from django.utils import timezone


class ClientThread(Thread):

    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn

    def run(self):
        # while True:
        data = self.conn.recv(10008)
        print("Received:", data)
        splitted_data = data.split("|")
        user_ = MyUser.objects.filter(id=splitted_data[0])[0]
        device_ = PhysicalNode.objects.filter(id=splitted_data[1])[0]

        valueRec = Values(varValue=splitted_data[4], timestamp=timezone.now(), usernameID=user_,
                          deviceID=device_, varname=splitted_data[2])
        valueRec.save(force_insert=True)
        # print len(splitted_data)  # 3
        # print splitted_data[0]  # mkyong.com
        # print splitted_data[1]  # 100
        # print splitted_data[2]  # 2015-10-1
        # self.conn.send('OK\r\n')
        num = 0
        p = output.objects.filter(deviceID_id=device_)
        num = p[0].value + p[1].value * 2
        # print 'OK|' + str(num)
        # self.conn.send('OK|')

        self.conn.send('OK\r\nOK|' + str(num))

    # MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")  # if MESSAGE == 'exit':  # break  # self.conn.send(MESSAGE)  # echo


class Command(BaseCommand):

    def handle(self, *args, **options):
        #    self.stdout.write('There are {} things!'.format(output.objects.count()))

        # Multithreaded Python server : TCP Server Socket Program Stub
        TCP_IP = '0.0.0.0'
        TCP_PORT = 10008
        BUFFER_SIZE = 20  # Usually 1024, but we need quick response

        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []

        while True:
            tcpServer.listen(4)
            print("Waiting Connection...")
            (conn, (ip, port)) = tcpServer.accept()

            newthread = ClientThread(ip, port, conn)
            newthread.start()
            threads.append(newthread)
        for t in threads:
            t.join()
