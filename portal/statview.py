# from federate.fed_backend import fed_start, fed_stop
# from portal.models import MyUser, PhysicalNode
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count, F, Sum
from django.utils import timezone
from portal.user_access_profile import UserAccessProfile
from portal.models import Account, Reservation, SimReservation, \
    MyUser, ReservationDetail, PhysicalNode, VirtualNode
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

class StatsView(LoginRequiredAutoLogoutView):
    template_name = "stats-view.html"

    def dispatch(self, *args, **kwargs):
        return super(StatsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        usera = UserAccessProfile(self.request)
        q = Account.objects.get(user_ref=usera.user_obj).quota_ref
        user_plan = q.quota_title
        user_quota_size = q.quota_size
        the_date = datetime.now(tz=timezone.get_current_timezone())  # timezone.now()
        curr_start = the_date.replace(day=1).replace(hour=0, minute=0, second=0)
        curr_end = last_day_of_month(datetime.today()).replace(hour=23, minute=59, second=59)
        # user_usage = get_month_usage_hr(usera.user_obj, the_date, 't')
        user_usage = get_month_usage_credit(usera.user_obj, the_date)
        user_usage_p = user_usage / user_quota_size * 100

        year_vl, year_vv = get_last_year(usera.user_obj, the_date, 'v')
        year_sl, year_sv = get_last_year(usera.user_obj, the_date, 's')
        year_l, year_v = get_last_year(usera.user_obj, the_date, 't')

        context = super(StatsView, self).get_context_data(**kwargs)
        context['user_plan'] = user_plan
        context['user_quota_size'] = user_quota_size
        context['user_usage'] = user_usage
        context['user_usage_p'] = user_usage_p
        context['curr_start'] = curr_start
        context['curr_end'] = curr_end
        context['year_vv'] = year_vv
        context['year_sv'] = year_sv
        context['year_l'] = year_l
        context['year_v'] = year_v

        context['username'] = UserAccessProfile(self.request).username  # the_user(self.request)
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


class StatsAdminView(LoginRequiredAutoLogoutView):
    template_name = "stats-a-view.html"

    def dispatch(self, *args, **kwargs):
        return super(StatsAdminView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)

        the_date = datetime.now(tz=timezone.get_current_timezone())  # datetime.today()
        year_l, year_v = get_total_last_year(the_date, 't')
        year_vl, year_vv = get_total_last_year(the_date, 'v')
        year_sl, year_sv = get_total_last_year(the_date, 's')
        # user_list, value_list = get_month_usage_by_users(None)
        res_l , res_v, res_c = get_total_resource_usage()

        context = super(StatsAdminView, self).get_context_data(**kwargs)
        context['year_l'] = year_l
        context['year_vv'] = year_vv
        context['year_sv'] = year_sv
        context['year_v'] = year_v
        context['res_l'] = res_l
        context['res_v'] = res_v
        context['res_c'] = res_c
        context['username'] = UserAccessProfile(self.request).username  # the_user(self.request)
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


def check_user_reserve(user_ref):
    q = Account.objects.get(user_ref=user_ref).quota_ref
    user_quota_size = q.quota_size
    the_date = datetime.now(tz=timezone.get_current_timezone())
    user_usage = get_month_usage_hr(user_ref, the_date, 't')
    return user_usage, user_quota_size


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def get_total_last_year(any_day, the_type):
    month_list = []
    value_list = []
    for i in range(0, 12):
        gday = any_day + relativedelta(months=-i)
        month_list.insert(0, gday.strftime('%B'))
        value_list.insert(0, get_month_usage_hr(None, gday, the_type))
    return month_list, value_list


def get_month_usage_hr(user_ref, any_day, the_type):
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)
    csum = 0

    if the_type is 'v' or the_type is 't':
        if user_ref:
            result1 = Reservation.objects.filter(user_ref=user_ref,
                                                 status__in=[3, 4],
                                                 start_time__gte=curr_start,
                                                 end_time__lte=curr_end)
        else:
            result1 = Reservation.objects.filter(status__in=[3, 4],
                                                 start_time__gte=curr_start,
                                                 end_time__lte=curr_end)
        for x in result1:
            csum += x.slice_duration

    if the_type is 's' or the_type is 't':
        if user_ref:
            result2 = SimReservation.objects.filter(user_ref=user_ref,
                                                    status__in=[3, 4],
                                                    start_time__gte=curr_start,
                                                    end_time__lte=curr_end)
        else:
            result2 = SimReservation.objects.filter(status__in=[3, 4],
                                                    start_time__gte=curr_start,
                                                    end_time__lte=curr_end)
        for x in result2:
            csum += x.slice_duration

    return csum


def get_month_usage_credit(user_ref, any_day):
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)
    csum = 0

    if user_ref:
        res1 = ReservationDetail.objects.filter(reservation_ref__user_ref=user_ref,
                                                reservation_ref__status__in=[3, 4],
                                                reservation_ref__start_time__gte=curr_start,
                                                reservation_ref__end_time__lte=curr_end) \
            .values('node_ref__device_ref__credit_value') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value'))
    else:
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4],
                                                reservation_ref__start_time__gte=curr_start,
                                                reservation_ref__end_time__lte=curr_end) \
            .values('node_ref__device_ref__credit_value') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value'))

    for x in res1:
        csum += x['sum']

    return csum


def get_usage_hr_by_users(the_sort, the_date):
    any_day = datetime.now(tz=timezone.get_current_timezone())
    k = 1  # months
    if the_sort == '2':
        the_sort = '-'
    else:
        the_sort = ''

    if the_date == 'y':
        k = 12
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0) + relativedelta(months=-k)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)

    if the_date == 'a':
        res1 = Reservation.objects.filter(status__in=[3, 4]) \
            .values('user_ref') \
            .annotate(sum=Sum('slice_duration')).order_by(the_sort + 'sum')
    else:
        res1 = Reservation.objects.filter(status__in=[3, 4], start_time__gte=curr_start, end_time__lte=curr_end) \
            .values('user_ref') \
            .annotate(sum=Sum('slice_duration')).order_by(the_sort + 'sum')

    o_list = []
    for r in res1:
        x = MyUser.objects.get(id=r['user_ref'])
        name = x.first_name + ' ' + x.last_name + " (" + x.username + ")"
        usage = r['sum']
        l = {'Total Usage (hr)': usage, 'User Name': name, }
        o_list.append(l)

    return o_list


def get_usage_cr_by_users(the_sort, the_date):
    any_day = datetime.now(tz=timezone.get_current_timezone())
    k = 1  # months
    if the_sort == '2':
        the_sort = '-'
    else:
        the_sort = ''

    if the_date == 'y':
        k = 12
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0) + relativedelta(months=-k)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)

    if the_date == 'a':
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4]) \
            .values('reservation_ref__user_ref') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value')).order_by(the_sort + 'sum')
    else:
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4],
                                                reservation_ref__start_time__gte=curr_start,
                                                reservation_ref__end_time__lte=curr_end) \
            .values('reservation_ref__user_ref') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value')).order_by(the_sort + 'sum')

    o_list = []
    for r in res1:
        x = MyUser.objects.get(id=r['reservation_ref__user_ref'])
        name = x.first_name + ' ' + x.last_name + " (" + x.username + ")"
        usage = r['sum']
        l = {'Total Credit': usage, 'User Name': name, }
        o_list.append(l)

    return o_list


def get_usage_hr_by_resources(the_sort, the_date):
    any_day = datetime.now(tz=timezone.get_current_timezone())
    k = 1  # months
    if the_sort == '2':
        the_sort = '-'
    else:
        the_sort = ''

    if the_date == 'y':
        k = 12
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0) + relativedelta(months=-k)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)

    if the_date == 'a':
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4]) \
            .values('node_ref') \
            .annotate(sum=Sum('reservation_ref__slice_duration')).order_by(the_sort + 'sum')
    else:
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4],
                                                reservation_ref__start_time__gte=curr_start,
                                                reservation_ref__end_time__lte=curr_end) \
            .values('node_ref') \
            .annotate(sum=Sum('reservation_ref__slice_duration')).order_by(the_sort + 'sum')

    # print(res1)
    o_list = []
    for r in res1:
        #print(r)
        x = VirtualNode.objects.get(id=r['node_ref'])
        name = x.vm_name
        usage = r['sum']
        l = {'Total Usage (hr)': usage, 'Node Name': name, }
        o_list.append(l)

    return o_list


def get_usage_cr_by_resources(the_sort, the_date):
    any_day = datetime.now(tz=timezone.get_current_timezone())
    k = 1  # months
    if the_sort == '2':
        the_sort = '-'
    else:
        the_sort = ''

    if the_date == 'y':
        k = 12
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0) + relativedelta(months=-k)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)

    if the_date == 'a':
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4]) \
            .values('node_ref') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value')).order_by(the_sort + 'sum')
    else:
        res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4],
                                                reservation_ref__start_time__gte=curr_start,
                                                reservation_ref__end_time__lte=curr_end) \
            .values('node_ref') \
            .annotate(sum=Sum('node_ref__device_ref__credit_value')).order_by(the_sort + 'sum')

    # print(res1)
    o_list = []
    for r in res1:
        #  print(r)
        x = VirtualNode.objects.get(id=r['node_ref'])
        name = x.vm_name
        usage = r['sum']
        l = {'Total Credit': usage, 'Node Name': name, }
        o_list.append(l)

    return o_list


def get_last_year(user_ref, any_day, the_type):
    month_list = []
    value_list = []
    for i in range(0, 12):
        gday = any_day + relativedelta(months=-i)
        month_list.insert(0, gday.strftime('%B'))
        value_list.insert(0, get_month_usage_hr(user_ref, gday, the_type))

    # month_list = ast.literal_eval(month_list.pop())
    return month_list, value_list


def get_total_resource_usage():
    res1 = ReservationDetail.objects.filter(reservation_ref__status__in=[3, 4]) \
            .values('node_ref') \
            .annotate(sum=Sum('reservation_ref__slice_duration'))
    r_list = []
    u_list = []
    for r in res1:
        x = VirtualNode.objects.get(id=r['node_ref'])
        name = x.vm_name
        usage = r['sum']
        #total += usage
        r_list.append(name)
        u_list.append(usage)

    c_list = ['#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
              for i in range(r_list.__len__())]
    return r_list, u_list , c_list


def stat_report(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    group_v = request.POST.get('the_group', None)
    order_v = request.POST.get('the_order', None)
    date_v = request.POST.get('the_date', None)
    type_v = request.POST.get('the_type', None)
    # curr_date = parser.parse(request.POST.get('the_date', timezone.now()))
    print(group_v, ' ', order_v, ' ', date_v, ' ', type_v)

    output = '<table class="table table-hover table-sm table-dark"><thead><tr><th scope="col">#</th>'
    count = 1
    olist = None

    if group_v == '1' and type_v == 'h':
        olist = get_usage_hr_by_users(order_v, date_v)
    elif group_v == '1' and type_v == 'c':
        olist = get_usage_cr_by_users(order_v, date_v)
    elif group_v == '3' and type_v =='h':
        olist = get_usage_hr_by_resources(order_v, date_v)
    elif group_v == '3' and type_v =='c':
        olist = get_usage_cr_by_resources(order_v, date_v)
    if olist:
        for k in olist[0]:
            output += '<th scope="col">' + k + '</th>'
        output += '</tr></thead><tbody><tr>'
        for i in olist:
            output += '<th scope="row">' + str(count) + '</th>'
            count += 1
            for k, v in i.items():
                output += '<td>' + str(v) + '</td>'
            output += '</tr>'

    output += '</tbody></table>'
    # print(output)
    if output:
        return HttpResponse(output, content_type="application/html")
    return HttpResponse('{"error":"0","msg":"error"}', content_type="application/json")
