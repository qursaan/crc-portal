import json
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

from portal.backend_actions import create_backend_user
from portal.models import Authority, MyUser, PendingSlice, \
    PendingAuthority, VirtualNode, \
    Reservation, ReservationDetail, SimReservation, SimulationVM


# Thierry: moving this right into the code so
# most people can use myslice without having to install sfa
# XXX tmp sfa dependency, should be moved to SFA gateway
# from sfa.util.xrn                import Xrn
# from manifold.core.query         import Query
# from manifold.manifoldapi        import execute_query,execute_admin_query


# ************* Default Scheduling Slice ************** #
def schedule_slice(slice_id):
    curr_slice = PendingSlice.objects.get(id=slice_id)
    request_time = curr_slice.created

    next_time = get_next_hour(request_time)
    overlap = PendingSlice.objects.filter(status=3, start_time=next_time)
    while overlap.exists():
        next_time = get_next_hour(next_time)
        overlap = PendingSlice.objects.filter(status=3, start_time=next_time)

    curr_slice.start_time = next_time
    curr_slice.end_time = get_next_hour(next_time)
    curr_slice.approve_date = datetime.now()
    curr_slice.status = 3
    curr_slice.save()
    return True


def schedule_auto_online(reserve_id, stype="omf"):
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
    curr_start = curr_slice.f_start_time
    last_end = curr_slice.f_end_time - timedelta(hours=dur)
    overlap_flag = False

    if last_end <= curr_start:
        last_end = curr_slice.f_end_time

    while curr_start <= last_end:
        curr_end = curr_start + timedelta(hours=dur)
        overlap = None
        overlap_flag = False
        if stype == "omf":
            overlap = Reservation.objects.filter(status=3, start_time__lte=curr_start, end_time__gte=curr_end)
            # check nodes
            for r in overlap:
                details = ReservationDetail.objects.filter(reservation_ref=r, node_ref__in=new_list)
                if details.exists():
                    overlap_flag = True
                    break

        elif stype == "sim":
            overlap = SimReservation.objects.filter(status=3, start_time__lte=curr_start, end_time__gte=curr_end, node_ref__in=new_list)

            if overlap.exists():
                overlap_flag = True

        if not overlap_flag:
            break
        else:
            curr_start = curr_start + timedelta(hours=1)

    # end search with time slot
    if curr_start < curr_slice.f_end_time:
        curr_slice.start_time   = curr_start
        curr_slice.end_time     = curr_end  # curr_start + timedelta(hours=dur)
        curr_slice.approve_date = timezone.now()
        curr_slice.status       = 3
        curr_slice.save()
        return True
    else:
        return False

""" 24801787
def schedule_sim_online(reserve_id):
    curr_slice = SimReservation.objects.get(id=reserve_id)
    dur = int(curr_slice.slice_duration)

    curr_time = curr_slice.f_start_time
    lst_end = curr_slice.f_end_time - timedelta(hours=dur)
    while curr_time <= lst_end:
        curr_end = curr_time + timedelta(hours=dur)
        overlap = SimReservation.objects.filter(status=3, start_time=curr_time, end_time=curr_end)
        # check nodes
        if not overlap.exists():
            break
        curr_time = curr_time + timedelta(hours=1)

    # end search with time slot
    if curr_time <= lst_end:
        curr_slice.start_time = curr_time
        curr_slice.end_time = curr_time + timedelta(hours=dur)
        curr_slice.approve_date = datetime.now()
        curr_slice.status = 3
        curr_slice.save()
        return True
    else:
        return False
"""


# to check time slot for omf testbeds
def checking_omf_time(nodelist, start_datetime, end_datetime):
    message = ""
    new_list = []
    for n in nodelist:
        new_list.append(int(n))
    curr_time = start_datetime
    while curr_time < end_datetime:
        overlap = Reservation.objects.filter(status=3, start_time__lte=curr_time, end_time__gte=curr_time)
        for r in overlap:
            nodes = VirtualNode.objects.filter(pk__in=new_list)
            details = ReservationDetail.objects.filter(reservation_ref=r).filter(node_ref__in=nodes)
            for d in details:
                d1 = utc_to_timezone(r.start_time).strftime("%Y-%m-%d %H:%M")
                d2 = utc_to_timezone(r.end_time).strftime("%Y-%m-%d %H:%M")
                message += "<li>Node: " + d.node_ref.vm_name + " Busy [" + d1 + " : " + d2 + "]</li>"
        curr_time = curr_time + timedelta(hours=1)
    if message:
        message = "<ul>" + message + "</ul>"
    return message


# to check time slot for simulation
def checking_sim_time(nodelist, start_datetime, end_datetime, slice_duration):
    message = ""
    curr_time = start_datetime
    lst_end = end_datetime - timedelta(hours=int(slice_duration))
    while curr_time < lst_end:
        curr_end = curr_time + timedelta(hours=int(slice_duration))
        nodes = SimulationVM.objects.filter(pk__in=nodelist)
        overlap = SimReservation.objects.filter(status=3, start_time__lte=curr_time, end_time__gte=curr_end, node_ref=nodes)

        for r in overlap:
            d1 = utc_to_timezone(r.start_time).strftime("%Y-%m-%d %H:%M")
            d2 = utc_to_timezone(r.end_time).strftime("%Y-%m-%d %H:%M")
            message += "<li>VM Node: " + r.vm_ref.vm_name + " Busy [" + d1 + " : " + d2 + "]</li>"
        curr_time = curr_time + timedelta(hours=1)
    if message:
        message = "<ul>" + message + "</ul>"
    return message


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
    active_list_1 = Reservation.objects.filter(user_ref=c_user, status=3)
    active_list_2 = SimReservation.objects.filter(user_ref=c_user, status=3)
    current_time = timezone.now()
    total_count = active_list_1.count() + active_list_2.count()
    # confirm active session
    for al in active_list_1:
        if al.end_time < current_time:
            al.status = 4
            al.save()
            total_count -= 1

    for al in active_list_2:
        if al.end_time < current_time:
            al.status = 4
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


# Get the list of authorities
"""
def authority_get_pis(request, authority_hrn):

    query = Query.get('authority').filter_by('authority_hrn', '==', authority_hrn).select('pi_users')
    results = execute_query(request, query)
    # NOTE: temporarily commented. Because results is giving empty list.
    # Needs more debugging
    #if not results:
    #    raise Exception, "Authority not found: %s" % authority_hrn
    #result, = results
    #return result['pi_users']
    return results

def authority_get_pi_emails(request, authority_hrn):
    #return ['jordan.auge@lip6.fr', 'loic.baron@lip6.fr']

    pi_users = authority_get_pis(request,authority_hrn)
    pi_user_hrns = [ hrn for x in pi_users for hrn in x['pi_users'] ]
    query = Query.get('user').filter_by('user_hrn', 'included', pi_user_hrns).select('email')
    results = execute_query(request, query)
    print "mails",  [result['email'] for result in results]
    return [result['email'] for result in results]

# SFA add record (user, slice)

def sfa_add_user(request, user_params):
    if 'email' in user_params:
        user_params['user_email'] = user_params['email']
    query = Query.create('user').set(user_params).select('user_hrn')
    results = execute_query(request, query)
    if not results:
        raise Exception, "Could not create %s. Already exists ?" % user_params['hrn']
    return results

def sfa_update_user(request, user_hrn, user_params):
    # user_params: keys [public_key]
    if 'email' in user_params:
        user_params['user_email'] = user_params['email']
    query = Query.update('user').filter_by('user_hrn', '==', user_hrn).set(user_params).select('user_hrn')
    results = execute_query(request,query)
    return results

def sfa_add_slice(request, slice_params):
    query = Query.create('slice').set(slice_params).select('slice_hrn')
    results = execute_query(request, query)
    if not results:
        raise Exception, "Could not create %s. Already exists ?" % slice_params['hrn']
    return results

def sfa_add_authority(request, authority_params):
    query = Query.create('authority').set(authority_params).select('authority_hrn')
    results = execute_query(request, query)
    print "sfa_add_auth results=",results
    if not results:
        raise Exception, "Could not create %s. Already exists ?" % authority_params['hrn']
    return results

def sfa_add_user_to_slice(request, user_hrn, slice_params):
# UPDATE myslice:slice SET researcher=['ple.upmc.jordan_auge','ple.inria.thierry_parmentelat','ple.upmc.loic_baron','ple.upmc.ciro_scognamiglio','ple.upmc.mohammed-yasin_rahman','ple.upmc.azerty'] where slice_hrn=='ple.upmc.myslicedemo'
    query_current_users = Query.get('slice').select('user').filter_by('slice_hrn','==',slice_params['hrn'])
    results_current_users = execute_query(request, query_current_users)
    slice_params['researcher'] = slice_params['researcher'] | results_current_users
    query = Query.update('slice').filter_by('user_hrn', '==', user_hrn).set(slice_params).select('slice_hrn')
    results = execute_query(request, query)
# Also possible but not supported yet
# UPDATE myslice:user SET slice=['ple.upmc.agent','ple.upmc.myslicedemo','ple.upmc.tophat'] where user_hrn=='ple.upmc.azerty'
    if not results:
        raise Exception, "Could not create %s. Already exists ?" % slice_params['hrn']
    return results

# Propose hrn

def manifold_add_user(request, user_params):
    # user_params: email, password e.g., user_params = {'email':'aa@aa.com','password':'demo'}
    query = Query.create('local:user').set(user_params).select('email')
    results = execute_admin_query(request, query)
    if not results:
        raise Exception, "Failed creating manifold user: %s" % user_params['email']
    result, = results
    return result['email']

def manifold_update_user(request, email, user_params):
    # user_params: password, config e.g.,
    query = Query.update('local:user').filter_by('email', '==', email).set(user_params).select('email')
    results = execute_admin_query(request,query)
    # NOTE: results remains empty and goes to Exception. However, it updates the manifold DB.
    # That's why I commented the exception part. -- Yasin
    #if not results:
    #    raise Exception, "Failed updating manifold user: %s" % user_params['email']
    #result, = results
    return results

def manifold_add_account(request, account_params):
    query = Query.create('local:account').set(account_params).select(['user', 'platform'])
    results = execute_admin_query(request,query)
    if not results:
        raise Exception, "Failed creating manifold account on platform %s for user: %s" % (account_params['platform'], account_params['user'])
    result, = results
    return result['user_id']

def manifold_update_account(request,user_id,account_params):
    # account_params: config
    query = Query.update('local:account').filter_by('platform', '==', 'myslice').filter_by('user_id', '==', user_id).set(account_params).select('user_id')
    results = execute_admin_query(request,query)
    return results

#explicitly mention the platform_id
def manifold_delete_account(request, platform_id, user_id, account_params):
    query = Query.delete('local:account').filter_by('platform_id', '==', platform_id).filter_by('user_id', '==', user_id).set(account_params).select('user_id')
    results = execute_admin_query(request,query)
    return results


#not tested
def manifold_add_platform(request, platform_params):
    query = Query.create('local:platform').set(platform_params).select(['user', 'platform'])
    results = execute_admin_query(request,query)
    if not results:
        raise Exception, "Failed creating manifold  platform %s for user: %s" % (platform_params['platform'], platform_params['user'])
    result, = results
    return result['platform_id']
"""


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
                # XXX tmp user_hrn inside the keypair column of pendiguser table
                ##                hrn = json.loads(request['keypair'])['user_hrn']
                # hrn = "%s.%s" % (request['authority_hrn'], request['login'])
                # XXX tmp sfa dependency
                # from sfa.util.xrn import Xrn
                ##                urn = Xrn(hrn, request['type']).get_urn()
                ##                if 'pi' in request:
                ##                    auth_pi = request['pi']
                ##                else:
                ##                    auth_pi = ''
                ##                sfa_user_params = {
                ##                    'hrn'        : hrn,
                ##                    'urn'        : urn,
                ##                    'type'       : request['type'],
                ##                    'keys'       : [json.loads(request['keypair'])['user_public_key']],
                ##                    'first_name' : request['first_name'],
                ##                    'last_name'  : request['last_name'],
                ##                    'email'      : request['email'],
                ##                    #'slices'    : None,
                ##                    #'researcher': None,
                ##                    'pi'         : [auth_pi],
                ##                    'enabled'    : True
                ##                }
                # ignored in request: id, timestamp, password

                # ADD USER TO SFA Registry
                ##                sfa_add_user(wsgi_request, sfa_user_params)

                # USER INFO
                ##                user_query  = Query().get('local:user').select('user_id','config','email','status').filter_by('email', '==', request['email'])
                ##                user_details = execute_admin_query(request, user_query)
                # print user_details[0]

                # UPDATE USER STATUS = 2
                ##                manifold_user_params = {
                ##                    'status': 2
                ##                }
                ##                manifold_update_user(request, request['email'], manifold_user_params)

                # USER MAIN ACCOUNT != reference
                # print 'USER MAIN ACCOUNT != reference'
                ##                list_accounts_query  = Query().get('local:account').select('user_id','platform_id','auth_type','config')\
                ##                    .filter_by('user_id','==',user_details[0]['user_id'])\
                ##                    .filter_by('auth_type','!=','reference')
                ##                list_accounts = execute_admin_query(request, list_accounts_query)
                ##                #print "List accounts = ",list_accounts
                ##                for account in list_accounts:
                ##                    main_platform_query  = Query().get('local:platform').select('platform_id','platform').filter_by('platform_id','==',account['platform_id'])
                ##                    main_platform = execute_admin_query(request, main_platform_query)

                # ADD REFERENCE ACCOUNTS ON SFA ENABLED PLATFORMS
                # print 'ADD REFERENCE ACCOUNTS ON SFA ENABLED PLATFORMS'
                ##                platforms_query  = Query().get('local:platform').filter_by('disabled', '==', '0').filter_by('gateway_type','==','sfa').select('platform_id','gateway_type')
                ##                platforms = execute_admin_query(request, platforms_query)
                ##                #print "platforms SFA ENABLED = ",platforms
                ##                for platform in platforms:
                ##                    #print "add reference to platform ",platform
                ##                    manifold_account_params = {
                ##                        'user_id': user_details[0]['user_id'],
                ##                        'platform_id': platform['platform_id'],
                ##                        'auth_type': 'reference',
                ##                        'config': '{"reference_platform": "' + main_platform[0]['platform'] + '"}',
                ##                    }
                ##                    manifold_add_account(request, manifold_account_params)
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
                    request_status['CRC user'] = {'status': False, 'description': 'Server Error'}

            except Exception, e:
                request_status['CRC user'] = {'status': False, 'description': str(e)}

        elif request['type'] == 'slice':
            try:
                """hrn = "%s.%s" % (request['authority_hrn'], request['slice_name'])
                # XXX tmp sfa dependency
                from sfa.util.xrn import Xrn
                urn = Xrn(hrn, request['type']).get_urn()

                # Add User to Slice if we have the user_hrn in pendingslice table
                if 'user_hrn' in request:
                    user_hrn = request['user_hrn']
                    print "Slice %s will be created for %s" % (hrn,request['user_hrn'])
                else:
                    user_hrn=''
                    print "Slice %s will be created without users %s" % (hrn)
                sfa_slice_params = {
                    'hrn'        : hrn,
                    'urn'        : urn,
                    'type'       : request['type'],
                    #'slices'    : None,
                    'researcher' : [user_hrn],
                    #'pi'        : None,
                    'enabled'    : True
                }
                # ignored in request: id, timestamp,  number_of_nodes, type_of_nodes, purpose

                sfa_add_slice(wsgi_request, sfa_slice_params)
                #sfa_add_user_to_slice(wsgi_request, user_hrn, sfa_slice_params)"""
                # up_slice = PendingSlice.objects.get()

                result = schedule_slice(request['id'])
                request_status['CRC slice'] = {'status': result}

            except Exception, e:
                request_status['CRC slice'] = {'status': False, 'description': str(e)}

        """elif request['type'] == 'authority':
            try:
                #hrn = "%s.%s" % (request['authority_hrn'], request['site_authority'])
                hrn = request['site_authority']
                # XXX tmp sfa dependency
                from sfa.util.xrn import Xrn
                urn = Xrn(hrn, request['type']).get_urn()

                sfa_authority_params = {
                    'hrn'        : hrn,
                    'urn'        : urn,
                    'type'       : request['type'],
                    #'pi'        : None,
                    'enabled'    : True
                }
                print "ADD Authority"
                sfa_add_authority(wsgi_request, sfa_authority_params)
                request_status['CRC authority'] = {'status': True }

            except Exception, e:
                request_status['CRC authority'] = {'status': False, 'description': str(e)}
        """
        # XXX Remove from Pendings in database

        status['%s__%s' % (request['type'], request['id'])] = request_status

    return status


def validate_action(request, **kwargs):
    ids = filter(None, kwargs['id'].split('/'))
    status = portal_validate_request(request, ids)
    json_answer = json.dumps(status)
    return HttpResponse(json_answer)  # , mimetype="application/json")

# Django and ajax
# http://djangosnippets.org/snippets/942/
