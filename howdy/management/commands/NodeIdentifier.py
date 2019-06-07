import subprocess
from threading import Thread
from django.core.management.base import BaseCommand
from howdy.models import Node_Phy_Details

'''
from subprocess import Popen, PIPE, STDOUT
import sys
import socket
from SocketServer import ThreadingMixIn
from howdy.models import output, Values
import sys
import os
import datetime
from portal.models import MyUser, PhysicalNode
from time import sleep
from unfold.page import Page
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portal.models import VirtualNode, PhysicalNode, MyUser, Reservation, ReservationDetail, VirtualNode
from howdy.models import Variable
from portal.backend_actions import get_vm_status
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu import topmenu_items, the_user
from datetime import datetime
from django.utils import timezone
'''
class Checkslices(Thread):

    def run(self):
        # while True:
        cm_ = 'ls /sys/class/tty'
        p1 = subprocess.check_output([cm_], stderr=subprocess.STDOUT, shell=True)
        print('Identifing  Nodes . . .')
        p = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for r in p:
            acmsport = 'ACM'+str(r)
            if acmsport not in p1:
                continue
            baudrate = 115200
            uploaded_file_url = acmsport

            cmd = "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega2560 -cwiring -P/dev/tty" + acmsport + " -b" + str(baudrate) + " -D -b115200 -Ueeprom:r:/root/crc-portal/crc-portal/eeprom/" + uploaded_file_url + ":i"
            p2 = subprocess.check_output([cmd], stderr=subprocess.STDOUT, shell=True)
            f = open('/root/crc-portal/crc-portal/eeprom/' + uploaded_file_url, "r")
            f.read(9)
            devid = int(f.read(2))
            print(str(devid)+' '+acmsport )

            obj = Node_Phy_Details.objects.get(deviceID=devid)
            obj.devicePort = acmsport
            obj.save()
            # p = Node_Phy_Details.objects.filter(deviceID__in=node_list.values_list('id'))

        # print('Found ' + str(p.count()) + ' Nodes ')

        # for r in p:
        #   acmsport = r.devicePort
        #  baudrate = r.deviceBaud
        # localRemote = r.DevType
        # deviceRbAddress = r.deviceRbAddress
        # if localRemote == 'L':
        #   print ('lOCALLY Clearing Code in ' + acmsport)
        #  uploaded_file_url = '/media/Blank_Dont_Remove.hex'
        # os.system(
        #    "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega2560 -cwiring -P/dev/tty" + acmsport + " -b" + baudrate + " -D -V -Uflash:w:/root/crc-portal/crc-portal" + uploaded_file_url + ":i")
        # else:
        #   print ('REMOTLY Clearing Code in ' + acmsport)
        #  os.system(
        #     './manage.py client ' + acmsport + ' ' + baudrate + ' ' + deviceRbAddress + ' /root/crc-portal/crc-portal' + uploaded_file_url)




class Command(BaseCommand):

    def handle(self, *args, **options):
        newthread = Checkslices()
        newthread.start()
