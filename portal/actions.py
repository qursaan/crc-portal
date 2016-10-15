import json
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

from portal.backend_actions import create_backend_user, create_slice
from portal.models import Authority, MyUser, PendingSlice, \
    PendingAuthority, VirtualNode,  FrequencyRanges, \
    Reservation, ReservationDetail, SimReservation, SimulationVM, ReservationFrequency
from reservation_status import ReservationStatus


# ************* Default Scheduling Slice ************** #
def schedule_slice(slice_id, use_bulk=False):
    curr_slice = PendingSlice.objects.get(id=slice_id)
    request_time = curr_slice.created
    busy_list = ReservationStatus.get_busy_list(use_bulk)

    next_time = get_next_hour(request_time)
    overlap = PendingSlice.objects.filter(status__in=busy_list, start_time=next_time)
    while overlap.exists():
        next_time = get_next_hour(next_time)
        overlap = PendingSlice.objects.filter(status__in=busy_list, start_time=next_time)

    curr_slice.start_time = next_time
    curr_slice.end_time = get_next_hour(next_time)
    curr_slice.approve_date = datetime.now()
    curr_slice.status = ReservationStatus.get_active()
    curr_slice.save()
    return True


def schedule_auto_online(reserve_id, stype="omf", use_bulk=False, reserve_type="R"):
    busy_list = ReservationStatus.get_busy_list(use_bulk)
    curr_slice = None
    new_list = []

    if stype == "omf":
        curr_slice = Reservation.objects.get(id=reserve_id)
        curr_detail = ReservationDetail.objects.filter(reservation_ref=curr_slice)
        for n in curr_detail:
            new_list.append(n.node_ref)

    elif stype == "sim":
        curr_slice = SimReservation.objects.get(id=reserve_id)
        new_list = [curr_slice.node_ref]

    dur = int(curr_slice.slice_duration)

    diff_time = curr_slice.f_end_time - curr_slice.f_start_time

    # if time-difference is less than duration set duration with difference time
    if timedelta(hours=dur) > diff_time > timedelta(hours=0):
        dur = diff_time
    elif diff_time <= timedelta(hours=0):
        dur = 1

    curr_start = curr_slice.f_start_time
    last_end = curr_slice.f_end_time - timedelta(hours=dur)
    # overlap_flag = False

    if last_end <= curr_start:
        last_end = curr_slice.f_end_time

    curr_end = None

    while curr_start <= last_end:
        curr_end = curr_start + timedelta(hours=dur)
        # overlap = None
        overlap_flag = False
        if stype == "omf":
            overlap = Reservation.objects.filter(status__in=busy_list, start_time__lte=curr_start, end_time__gte=curr_end)
            # check nodes
            for r in overlap:
                details = ReservationDetail.objects.filter(reservation_ref=r, node_ref__in=new_list)
                if details.exists():
                    overlap_flag = True
                    break

        elif stype == "sim":
            overlap = SimReservation.objects.filter(status__in=busy_list, start_time__lte=curr_start, end_time__gte=curr_end,
                                                    node_ref__in=new_list)

            if overlap.exists():
                overlap_flag = True

        if not overlap_flag:
            break
        else:
            curr_start = curr_start + timedelta(hours=1)

    # end search with time slot
    if curr_start < curr_slice.f_end_time:
        curr_slice.start_time = curr_start
        curr_slice.end_time = curr_end  # curr_start + timedelta(hours=dur)
        if use_bulk:
            curr_slice.start_time = curr_slice.f_start_time
            curr_slice.end_time = curr_slice.f_end_time

        curr_slice.approve_date = timezone.now()
        if reserve_type == "R":
            curr_slice.status = ReservationStatus.get_active()
        elif reserve_type == "I":
            curr_slice.status = ReservationStatus.get_bulk()
        curr_slice.save()

        node_list = []
        for n in new_list:
            node_list.append(n.vm_name)
        output = create_slice(curr_slice.user_ref.username, utc_to_timezone(curr_start), utc_to_timezone(curr_end), node_list)
        if output == 1:
            return True
        else:
            curr_slice.status = ReservationStatus.get_pending()
            curr_slice.save()
            return False
    else:
        return False


def schedule_checking(nodelist, start_datetime, end_datetime, stype="omf", use_bulk=False):
    new_list = []
    for n in nodelist:
        new_list.append(int(n))

    curr_start = start_datetime
    curr_end = end_datetime

    busy_list = ReservationStatus.get_busy_list(use_bulk)
    overlap = None
    node_list = []
    output_list = ""

    if stype == "omf":
        node_list = VirtualNode.objects.filter(pk__in=new_list)
        overlap = ReservationDetail.objects.filter(
            reservation_ref__status__in=busy_list, node_ref__in=node_list)  # .filter(
        # Q(reservation_ref__start_time__gte=curr_start) | Q(reservation_ref__end_time__lt=curr_end))
    elif stype == "sim":
        node_list = SimulationVM.objects.filter(pk__in=nodelist)
        overlap = SimReservation.objects.filter(status__in=busy_list, node_ref__in=node_list)  # .filter(
        # Q(start_time__gte=curr_start) | Q(end_time__lt=curr_end))

    for n in node_list:
        for r in overlap:
            if r.node_ref.id == n.id:
                # t1 = t2 = None

                # correct ref
                if stype == "omf":
                    r = r.reservation_ref

                # case 0: assume  start & end between s and e
                t1 = r.start_time
                t2 = r.end_time

                # case 1: if end & start out  s and e then discard
                if t1 < t2 <= curr_start or curr_end <= t1 < t2:
                    continue

                d1 = utc_to_timezone(r.start_time).strftime("%Y-%m-%d %H:%M")
                d2 = utc_to_timezone(r.end_time).strftime("%Y-%m-%d %H:%M")
                z = "<li>Node: " + str(n) + " Busy [" + d1 + " : " + d2 + "]</li>"

                # output_list.append(z)
                output_list += z
    if output_list:
        output_list = "<ul>" + output_list + "</ul>"
    return output_list


def schedule_checking_all(start_datetime, end_datetime, stype="omf"):
    curr_start = start_datetime
    curr_end = end_datetime

    busy_list = ReservationStatus.get_busy_list()
    overlap = None
    node_list = []
    # busy_list = []

    if stype == "omf":
        node_list = VirtualNode.objects.all()
        overlap = ReservationDetail.objects.filter(
            reservation_ref__status__in=busy_list, node_ref__in=node_list)
    elif stype == "sim":
        node_list = SimulationVM.objects.all()
        overlap = SimReservation.objects.filter(status__in=busy_list, node_ref__in=node_list)

    for n in node_list:
        for r in overlap:
            if r.node_ref.id == n.id:
                # t1 = t2 = None

                # correct ref
                if stype == "omf":
                    r = r.reservation_ref

                # case 0: assume  start & end between s and e
                t1 = r.start_time
                t2 = r.end_time

                # case 1: if end & start out  s and e then discard
                if t1 < t2 <= curr_start or curr_end <= t1 < t2:
                    continue

                busy_list += n.id

    return busy_list


def schedule_checking_freq(freq_list, start_datetime, end_datetime, use_bulk=False):

    new_list = []
    for n in freq_list:
        new_list.append(int(n))

    curr_start = start_datetime
    curr_end = end_datetime

    busy_list = ReservationStatus.get_busy_list(use_bulk)
    output_list = ""
    freq_list = FrequencyRanges.objects.filter(pk__in=new_list)

    overlap = ReservationFrequency.objects.filter(
        reservation_ref__status__in=busy_list,
        frequency_ref__in=freq_list)

    for r in overlap:
        t1 = t2 = None

        # case 0: assume  start & end between s and e
        t1 = r.reservation_ref.start_time
        t2 = r.reservation_ref.end_time

        # case 1: if end & start out  s and e then discard
        if t1 < t2 <= curr_start or curr_end <= t1 < t2:
            continue

        d1 = utc_to_timezone(r.reservation_ref.start_time).strftime("%Y-%m-%d %H:%M")
        d2 = utc_to_timezone(r.reservation_ref.end_time).strftime("%Y-%m-%d %H:%M")
        z = "<li>Frequency: " + str(r.frequency_ref) + " Busy [" + d1 + " : " + d2 + "]</li>"

        # output_list.append(z)
        output_list += z

    if output_list:
        output_list = "<ul>" + output_list + "</ul>"

    return output_list


def utc_to_timezone(utc):
    current_tz = str(timezone.get_current_timezone())  # ="Africa/Cairo"
    return utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(current_tz))


# ************* Get Next Free Hour/Day **************** #
def get_next_hour(request_time):
    request_time = request_time + timedelta(hours=1)
    next_time = request_time.replace(minute=0, second=0, microsecond=0)
    return next_time


# ************* Get User Object by Email ************** #
def get_user_by_email(u_email):
    user = MyUser.objects.filter(email__iexact=u_email)
    if user:
        return user[0]
    return None


def get_username_by_email(u_email):
    user = MyUser.objects.filter(email__iexact=u_email)
    if user:
        return user[0].username
    return None


def get_user_type(c_user):
    if c_user:
        if c_user.user_type:
            return c_user.user_type
        return 0
    return -1


# ************* Get Task Id by Slice Id *************** #
def get_task_id(slice_id, node_name, stype):
    if stype == "omf":
        curr_slice = Reservation.objects.get(id=slice_id)
        node = VirtualNode.objects.get(vm_name=node_name)
        res_detail = ReservationDetail.objects.filter(reservation_ref=curr_slice, node_ref=node)
        if res_detail:
            return res_detail[0].id
    elif stype == "sim":
        return slice_id
    return None


def update_task_testbed(task_id, action, stype):
    res = None
    if stype == "omf":
        res = ReservationDetail.objects.get(id=task_id)
    elif stype == "sim":
        res = SimReservation.objects.get(id=task_id)

    if res:
        res.last_action = datetime.now()
        res.details = action
        res.save()
        return True
    return False


def check_next_task_duration(task_id, stype):
    if stype == "omf":
        res = ReservationDetail.objects.get(id=task_id)
        last_time = res.last_action
        curr_time = timezone.now()
        if last_time:
            next_time = last_time + timedelta(minutes=5)
            return next_time < curr_time
    elif stype == "sim":
        res = SimReservation.objects.get(id=task_id)
        last_time = res.last_action
        curr_time = timezone.now()
        if last_time:
            next_time = last_time + timedelta(minutes=5)
            return next_time < curr_time
    return True


def get_count_active_slice(c_user):
    busy_list = ReservationStatus.get_busy_list(allow_bulk=True, allow_pending=True)
    active_list_1 = Reservation.objects.filter(user_ref=c_user, status__in=busy_list)
    active_list_2 = SimReservation.objects.filter(user_ref=c_user, status__in=busy_list)
    current_time = timezone.now()
    total_count = active_list_1.count() + active_list_2.count()
    # confirm active session
    for al in active_list_1:
        if al.end_time < current_time:
            al.status = ReservationStatus.get_expired()
            al.save()
            total_count -= 1

    for al in active_list_2:
        if al.end_time < current_time:
            al.status = ReservationStatus.get_expired()
            al.save()
            total_count -= 1

    return total_count



# ************* Get Authority by User email *********** #
def get_authority_by_user(username):
    ba = MyUser.objects.filter(email=username)
    if ba is not None:
        return ba[0].authority_hrn
    else:
        return None


# ************* Get Authority Email ******************* #
def get_authority_emails(authority):
    au = Authority.objects.filter(authority_hrn=authority)
    if au is not None:
        return [au[0].email]
    else:
        return ['qursaan@crclab.org']


# ************* Update Node Status ******************* #
def update_node_status(node_id, new_status):
    node = VirtualNode.objects.get(vm_name=node_id)
    if node is not None:
        if node.status != new_status:
            node.status = new_status
            node.save()
        return 1
    else:
        return 0


# ******** Generate user request from user Object ***** #
def make_request_user(user):
    request = {}
    request['type'] = 'user'
    request['id'] = user.id
    request['timestamp'] = user.created  # XXX in DB ?
    request['authority_hrn'] = user.authority_hrn
    request['first_name'] = user.first_name
    request['last_name'] = user.last_name
    request['email'] = user.email
    request['login'] = user.username  # login
    request['keypair'] = user.keypair
    return request


# ******** Generate slice request from slice Object *** #
def make_request_slice(c_slice):
    request = {}
    request['type'] = 'slice'
    request['id'] = c_slice.id
    request['user_hrn'] = c_slice.user_hrn
    request['timestamp'] = c_slice.created
    request['request_date'] = c_slice.request_date
    request['authority_hrn'] = c_slice.authority_hrn
    request['slice_name'] = c_slice.slice_name
    request['number_of_nodes'] = c_slice.number_of_nodes
    # request['type_of_nodes'] = slice.type_of_nodes
    request['purpose'] = c_slice.purpose
    return request


# ******** Generate auth request from auth Object ***** #
def make_request_authority(authority):
    request = {}
    request['type'] = 'authority'
    request['id'] = authority.id
    request['site_name'] = authority.site_name
    request['site_latitude'] = authority.site_latitude
    request['site_longitude'] = authority.site_longitude
    request['site_url'] = authority.site_url
    request['site_authority'] = authority.site_authority
    request['site_abbreviated_name'] = authority.site_abbreviated_name
    # request['address_line1']         = authority.address_line1
    # request['address_line2']         = authority.address_line2
    # request['address_line3']         = authority.address_line3
    request['address_city'] = authority.address_city
    request['address_postalcode'] = authority.address_postalcode
    request['address_state'] = authority.address_state
    request['address_country'] = authority.address_country
    request['authority_hrn'] = authority.authority_hrn
    request['timestamp'] = authority.created
    return request


# ******** Put all request in one variable ************ #
def make_requests(pending_users, pending_slices, pending_authorities):
    requests = []
    for _user in pending_users:
        requests.append(make_request_user(_user))
    for _slice in pending_slices:
        requests.append(make_request_slice(_slice))
    for _authority in pending_authorities:
        requests.append(make_request_authority(_authority))
    return requests


# ******** Get request by user id ********************* #
def get_request_by_id(ids):
    sorted_ids = {'user': [], 'slice': [], 'authority': []}
    for type__id in ids:
        type, id = type__id.split('__')
        sorted_ids[type].append(id)

    if not ids:
        pending_users = MyUser.objects.filter(status=1).all()
        pending_slices = PendingSlice.filter(status=1).objects.all()
        pending_authorities = PendingAuthority.objects.all()
    else:
        pending_users = MyUser.objects.filter(id__in=sorted_ids['user'], status=1).all()
        pending_slices = PendingSlice.objects.filter(id__in=sorted_ids['slice'], status=1).all()
        pending_authorities = PendingAuthority.objects.filter(id__in=sorted_ids['authority']).all()

    return make_requests(pending_users, pending_slices, pending_authorities)


# ******** Get request by authority hrn *************** #
def get_requests(authority_hrns=None):
    print "get_request_by_authority auth_hrns = ", authority_hrns
    if not authority_hrns:
        pending_users = MyUser.objects.filter(status=1).all()
        pending_slices = PendingSlice.objects.filter(status=1).all()
        pending_authorities = PendingAuthority.objects.all()
    else:
        pending_users = MyUser.objects.filter(authority_hrn__in=authority_hrns, status=1).all()
        pending_slices = PendingSlice.objects.filter(authority_hrn__in=authority_hrns, status=1).all()
        pending_authorities = PendingAuthority.objects.filter(authority_hrn__in=authority_hrns).all()

    return make_requests(pending_users, pending_slices, pending_authorities)


# XXX Is it in sync with the form fields ?
def portal_validate_request(wsgi_request, request_ids):
    status = {}

    if not isinstance(request_ids, list):
        request_ids = [request_ids]

    requests = get_request_by_id(request_ids)
    for request in requests:
        # type, id, timestamp, details, allowed -- MISSING: authority_hrn
        # CAREFUL about details
        # user  : first name, last name, email, password, keypair
        # slice : number of nodes, type of nodes, purpose

        request_status = {}

        print "REQUEST", request
        if request['type'] == 'user':

            try:
                up_user = MyUser.objects.get(id=request['id'])
                web_user = User.objects.get(id=up_user.id)
                # TODO: Create user file here
                result = create_backend_user(up_user.username, up_user.password)
                if result == 1:
                    up_user.status = 2
                    up_user.save()
                    web_user.is_active = True
                    web_user.save()

                    request_status['CRC user'] = {'status': True}
                else:
                    request_status['CRC user'] = {'status': False, 'description': 'Back Server Error'}

            except Exception, e:
                request_status['CRC user'] = {'status': False, 'description': str(e)}

        elif request['type'] == 'slice':
            try:
                result = schedule_slice(request['id'])
                request_status['CRC slice'] = {'status': result}

            except Exception, e:
                request_status['CRC slice'] = {'status': False, 'description': str(e)}

        status['%s__%s' % (request['type'], request['id'])] = request_status

    return status


def validate_action(request, **kwargs):
    ids = filter(None, kwargs['id'].split('/'))
    status = portal_validate_request(request, ids)
    json_answer = json.dumps(status)
    return HttpResponse(json_answer)  # , mimetype="application/json")

# Django and ajax
# http://djangosnippets.org/snippets/942/
