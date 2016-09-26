__author__ = 'qursaan'

import json
from datetime import timedelta
from dateutil import parser

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from lab.models import Course, Experiments, StudentsExperiment
from portal.actions import get_authority_by_user, get_user_by_email, get_user_type, \
    schedule_checking, schedule_checking_freq, schedule_auto_online
from portal.models import Reservation, ReservationDetail, ReservationFrequency,SimReservation
from portal.reservation_status import ReservationStatus
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class StudentReserveView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request, exp=None):
        return self.get_or_post(request, 'POST', exp)

    def get(self, request, exp=None):
        return self.get_or_post(request, 'GET', exp)

    def get_or_post(self, request, method, exp_id):
        self.user_email = the_user(request)
        page = Page(request)

        self.errors = []
        # print "EXP:", exp_id

        user = get_user_by_email(the_user(self.request))
        user_type = get_user_type(user)
        if user_type != 3 or exp_id is None:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        exp = Experiments.objects.get(id=exp_id)
        max_duration = exp.max_duration
        start_time = None
        end_time = None

        if exp.server_type == "omf":
            start_time = exp.reservation_ref.start_time
            end_time = exp.reservation_ref.end_time
        elif exp.server_type == "sim":
            start_time = exp.sim_reservation_ref.start_time
            end_time = exp.sim_reservation_ref.end_time

        s = None

        if method == 'POST':
            self.errors = []

            request_date = timezone.now()  # request.POST.get('request_date', '')
            authority_hrn = get_authority_by_user(the_user(request))

            purpose = request.POST.get('ex_detail', '')
            # date
            start_date = request.POST.get('req_time_date1', '')
            start_date = parser.parse(start_date)
            end_date = request.POST.get('req_time_date2', '')
            end_date = parser.parse(end_date)
            # time
            start_time = request.POST.get('req_time_time1', '')
            end_time = request.POST.get('req_time_time2', '')

            h1 = int(parser.parse(start_time).strftime('%H'))
            h2 = int(parser.parse(end_time).strftime('%H'))
            m1 = int(parser.parse(start_time).strftime('%M'))
            m2 = int(parser.parse(end_time).strftime('%M'))

            start_datetime = start_date + timedelta(hours=h1, minutes=m1)
            end_datetime = end_date + timedelta(hours=h2, minutes=m2)

            diff = end_datetime - start_datetime
            dur = diff.seconds / 60 / 60
            slice_duration = request.POST.get('max_duration', dur)


            if request_date is None or request_date == '':
                self.errors.append('Please, determine the request date and time')
            if purpose is None or purpose == '':
                self.errors.append('Purpose is mandatory')

            if not self.errors:
                exp = Experiments.objects.get(id=exp_id)
                if exp.server_type == "omf":
                    s = Reservation(
                        user_ref=user,
                        f_start_time=start_datetime,
                        f_end_time=end_datetime,
                        slice_name=exp.reservation_ref.slice_name,
                        slice_duration=slice_duration,  # approve_date
                        request_date=request_date,
                        authority_hrn=authority_hrn,
                        request_type=exp.reservation_ref.request_type,
                        base_image_ref=exp.reservation_ref.base_image_ref,  # ref
                        purpose=purpose,
                        status=ReservationStatus.get_pending(),
                    )
                    s.save()
                    resources = ReservationDetail.objects.filter(reservation_ref=exp.reservation_ref)
                    for i in resources:
                        p = ReservationDetail(
                            reservation_ref=s,
                            node_ref=i.node_ref,
                            image_ref=i.image_ref,
                        )
                        p.save()
                    freq_group = ReservationFrequency.objects.filter(reservation_ref=exp.reservation_ref)
                    for i in freq_group:
                        p = ReservationFrequency(
                            reservation_ref=s,
                            frequency_ref=i.frequency_ref
                        )
                        p.save()

                    # TODO: @qursaan
                    if not schedule_auto_online(s.id, "omf", use_bulk=True, reserve_type="R"):
                        self.errors.append('Sorry, Time slot is not free')
                        s.delete()

                elif exp.server_type == "sim":
                    s = SimReservation(
                        user_ref=user,
                        slice_name=exp.sim_reservation_ref.slice_name,
                        slice_duration=slice_duration,  # approve_date
                        request_date=request_date,
                        f_start_time=start_datetime,
                        f_end_time=end_datetime,
                        authority_hrn=authority_hrn,
                        request_type=exp.sim_reservation_ref.request_type,
                        image_ref=exp.sim_reservation_ref.image_ref,  # ref
                        node_ref=exp.sim_reservation_ref.node_ref,  # ref
                        purpose=purpose,
                        status=ReservationStatus.get_pending(),
                        n_processor=exp.sim_reservation_ref.sim_no_proc,
                        n_ram=exp.sim_reservation_ref.sim_ram_size,
                    )
                    s.save()
                    # TODO: @qursaan
                    if not schedule_auto_online(s.id, "sim",use_bulk=True,reserve_type="R"):
                        self.errors.append('Sorry, Time slot is not free')
                        s.delete()

            if not self.errors:
                # save experiment
                se = StudentsExperiment(
                    students_ref=user,
                    experiment_ref=exp,
                    start_time=start_datetime,
                    end_time=end_datetime,
                    status=0,
                )
                if exp.server_type == "omf":
                    se.reservation_ref = s
                elif exp.server_type == "sim":
                    se.sim_reservation_ref = s
                se.save()

                template_env = {
                    'topmenu_items': topmenu_items('test_page', request),
                    'username': the_user(request),
                    'title': 'Request',
                }
                template_env.update(page.prelude_env())
                return render(request, 'slice-request-ack-view.html', template_env)  # Redirect after POST

        template_name = "std-experiments-add.html"
        template_env = {
            'topmenu_items': topmenu_items('Reserve Experiment', page.request),
            'username': the_user(self.request),
            'ex_title': exp.title,
            'exp_id': exp_id,
            'max_duration': max_duration,
            'start_date': start_time,
            'end_date': end_time,
            'title': 'Reserve Experiment',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def check_availability_bulk(request):
    # print "Check BULK"
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    # exp
    exp_id = request.POST.get('exp', '')
    # date
    start_date = request.POST.get('date1', '')
    start_date = parser.parse(start_date)
    end_date = request.POST.get('date2', '')
    end_date = parser.parse(end_date)
    # time
    start_time = request.POST.get('time1', '')
    end_time = request.POST.get('time2', '')

    # duration
    dur = request.POST.get('dur', '1')

    h1 = int((parser.parse(start_time).strftime('%H')))
    h2 = int((parser.parse(end_time).strftime('%H')))
    m1 = int((parser.parse(start_time).strftime('%M')))
    m2 = int((parser.parse(end_time).strftime('%M')))

    start_datetime = timezone.make_aware(start_date + timedelta(hours=h1, minutes=m1))
    end_datetime = timezone.make_aware(end_date + timedelta(hours=h2, minutes=m2))

    exp = Experiments.objects.get(id=exp_id)
    the_type = exp.server_type

    if the_type == "omf":
        if exp.reservation_ref.start_time > start_datetime and exp.reservation_ref.end_time > end_datetime :
            msg = "<ul><li>Selected time is exceed the bulk range time .</li></ul>"
        else:
            nodes = ReservationDetail.objects.filter(reservation_ref=exp.reservation_ref)
            the_nodes = []
            for n in nodes:
                the_nodes.append(n.node_ref.id)

            freq = ReservationFrequency.objects.filter(reservation_ref=exp.reservation_ref)
            the_freq = []
            for f in freq:
                the_freq.append(f.frequency_ref.id)

            msg = schedule_checking(the_nodes, start_datetime, end_datetime, "omf", use_bulk=True)
            if the_freq:
                msg += schedule_checking_freq(the_freq, start_datetime, end_datetime, use_bulk=True)

    elif the_type == "sim":
        if exp.sim_reservation_ref.start_time > start_datetime and exp.sim_reservation_ref.end_time > end_datetime :
            msg = "<ul><li>Selected time is exceed the bulk range time .</li></ul>"
        else:
            nodes = SimReservation.objects.get(id=exp.sim_reservation_ref.id)
            the_nodes = nodes.node_ref.id
            msg = schedule_checking(the_nodes, start_datetime, end_datetime, "sim", use_bulk=True)

    free = "0"
    if not msg:
        msg = "Free"
        free = "1"

    output = {
        "free": free,
        "msg": msg,
        # "busy": busy_list
    }

    post_data = json.dumps(output)
    return HttpResponse(post_data, content_type="application/json")
