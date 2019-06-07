import os
from threading import Thread
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from howdy.models import Node_Phy_Details
from portal.models import PhysicalNode
from portal.models import Reservation, ReservationDetail, VirtualNode

'''
import socket
import datetime
from SocketServer import ThreadingMixIn
from howdy.models import output, Values
import sys
from howdy.models import Variable
from unfold.page import Page
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portal.backend_actions import get_vm_status
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu import topmenu_items, the_user
from datetime import datetime
'''


class Checkslices(Thread):

    def run(self):
        while True:
            print('Updating Slices . . .')

            vm_list = VirtualNode.objects.all().order_by('node_ref')

            # get all active reservations

            active_reservations = Reservation.objects.filter(f_start_time__lte=timezone.now(),
                                                             f_end_time__gt=timezone.now())
            print(active_reservations.values_list('f_start_time'))

            reservations_detail = ReservationDetail.objects.filter(reservation_ref=active_reservations).values_list(
                'node_ref_id')
            virtualnodes = VirtualNode.objects.filter(pk__in=reservations_detail).values_list('node_ref_id')

            # print (virtualnodes)

            node_list = PhysicalNode.objects.exclude(pk__in=virtualnodes)  # all()#

            # active S
            # print (node_list.values_list('id'))

            # inactive S
            p = Node_Phy_Details.objects.filter(deviceID__in=node_list.values_list('id'))
            # acmsport = p.devicePort
            # baudrate = p.deviceBaud
            print('Found ' + str(p.count()) + ' Inactive Slices')

            for r in p:
                did = r.deviceID_id
                acmsport = r.devicePort
                baudrate = r.deviceBaud
                localRemote = r.DevType
                deviceRbAddress = r.deviceRbAddress
                if localRemote == 'L':
                    print('lOCALLY Clearing Code in Node ' + str(did))
                    uploaded_file_url = '/media/Blank_Dont_Remove.hex'
                    os.system(
                        "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega2560 -cwiring -P/dev/tty" + acmsport + " -b" + baudrate + " -D -V -Uflash:w:/root/crc-portal/crc-portal" + uploaded_file_url + ":i")
                else:
                    print('REMOTLY Clearing Code in ' + str(did))
                    os.system('./manage.py client ' + str(
                        did) + ' ' + baudrate + ' ' + deviceRbAddress + ' /root/crc-portal/crc-portal' + uploaded_file_url)
                    print('./manage.py client ' + str(
                        did) + ' ' + baudrate + ' ' + deviceRbAddress + ' /root/crc-portal/crc-portal' + uploaded_file_url)
            # print(acmsport + baudrate)

            # 0x1e9801
            #
            sleep(5000)


class Command(BaseCommand):

    def handle(self, *args, **options):
        newthread = Checkslices()
        newthread.start()
