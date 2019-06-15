__author__ = 'pirate'

import json
from datetime import timedelta

from dateutil import parser
# from dateutil.parser import parse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from portal.actions import utc_to_timezone
from portal.models import SimReservation, VirtualNode, SimulationVM, \
    ReservationDetail
from portal.user_access_profile import UserAccessProfile
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
from .reservation_status import ReservationStatus
from crc.settings import SIM_RESERVATION


class SchedulerView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        usera = UserAccessProfile(request)
        self.user_email = usera.username # the_user(request)
        page = Page(request)

        server_type = "omf"
        request_date = timezone.now()

        if request.POST:  # method == 'POST':
            self.errors = []
            request_date = request.POST.get('request_date', timezone.now())
            server_type = request.POST.get('server_type', 'omf')
            request_date = parser.parse(request_date)

        # node_list = get_node_list(server_type)
        reserve_list = get_reservation_list(server_type, request_date)

        template_env = {
            #'topmenu_items': topmenu_items('Scheduler View', page.request),
            'username': usera.username,
            'server_type': request.POST.get('server_type', server_type),
            'sim_enable': SIM_RESERVATION,
            'errors': self.errors,
            'title': "Scheduler View",
            'request_date': request_date,
            # 'node_list': node_list,
            'reserve_list': reserve_list,
        }
        template_env.update(page.prelude_env())
        return render(request, 'scheduler-view.html', template_env)


def get_reservation_list(server_type, request_date):
    status = ReservationStatus.get_all_list() # [4, 3, 1]
    output_list = get_reservation_status_list(server_type, request_date, status)
    return json.dumps(output_list)


def get_reservation_status_list(server_type, request_date, status):
    day_start = utc_to_timezone(request_date).replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1) - timedelta(seconds=1)
    node_list = []
    reserve_list = []
    output_list = []
    # day_start_aware = (day_start)
    # day_end_aware = (day_end)

    if server_type == "omf":
        node_list = VirtualNode.objects.order_by('node_ref', 'hv_name')
        reserve_list = ReservationDetail.objects.filter(
            reservation_ref__status__in=status).filter(
            Q(reservation_ref__start_time__gte=day_start) | Q(reservation_ref__end_time__lt=day_end))

    elif server_type == "sim":
        node_list = SimulationVM.objects.all()
        reserve_list = SimReservation.objects.filter(status__in=status).filter(
            Q(start_time__gte=day_start) | Q(end_time__lt=day_end))

    # build output for time line
    for n in node_list:
        y = {}
        x = []
        for r in reserve_list:
            if r.node_ref.id == n.id:
                # t1 = t2 = None

                # correct ref
                if server_type == "omf":
                    r = r.reservation_ref

                # case 0: assume  start & end between s and e
                t1 = utc_to_timezone(r.start_time)
                t2 = utc_to_timezone(r.end_time)

                # case 1: if end & start out  s and e then discard
                if t1 < t2 < day_start or day_end < t1 < t2:
                    continue

                # case 2: if start earlier & end between  s and e change start
                if t1 <= day_start <= t2 <= day_end:
                    t1 = day_start

                # case 3: if end later & start between  s and e change end
                if day_start <= t1 <= day_end < t2:
                    t2 = day_end

                z = {
                    'id': str(r.id),
                    'title': str(r.user_ref),
                    'start': t1.strftime('%H:%M'),
                    'end': t2.strftime('%H:%M')
                }

                if r.status == ReservationStatus.get_active():
                    z['class'] = 'reserved'
                elif r.status == ReservationStatus.get_expired():
                    z['class'] = 'expired'
                elif r.status == ReservationStatus.get_pending():
                    z['class'] = 'pending'
                elif r.status == ReservationStatus.get_bulk():
                    z['class'] = 'bulk'
                elif r.status == ReservationStatus.get_canceled():
                    z['class'] = 'canceled'

                x.append(z)
        # end for appointments
        y['name'] = str(n)
        y['appointments'] = x
        output_list.append(y)
        # end for nodes

    # print json.dumps(output_list)
    return output_list


def check_scheduler(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    stype = request.POST.get('the_type', None)
    curr_date = parser.parse(request.POST.get('the_date', timezone.now()))
    output = get_reservation_list(stype, curr_date)
    if output:
        return HttpResponse(output, content_type="application/json")
    return HttpResponse('{"error":"0","msg":"error"}', content_type="application/json")
