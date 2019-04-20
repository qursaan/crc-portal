# from federate.fed_backend import fed_start, fed_stop
from portal.models import MyUser, PhysicalNode
from portal.user_access_profile import UserAccessProfile
from portal.models import Account, Reservation
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import ast


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
        curr_start = datetime.today().replace(day=1).replace(hour=0, minute=0, second=0)
        curr_end = last_day_of_month(datetime.today()).replace(hour=23, minute=59, second=59)
        user_usage = getMonthUsage(usera.user_obj, datetime.today())
        user_usage_p = user_usage / user_quota_size * 100

        year_l, year_v = getLastYear(usera.user_obj, datetime.today())

        context = super(StatsView, self).get_context_data(**kwargs)
        context['user_plan'] = user_plan
        context['user_quota_size'] = user_quota_size
        context['user_usage'] = user_usage
        context['user_usage_p'] = user_usage_p
        context['curr_start'] = curr_start
        context['curr_end'] = curr_end
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

        year_l, year_v = getTotalLastYear(datetime.today())

        context = super(StatsAdminView, self).get_context_data(**kwargs)
        context['year_l'] = year_l
        context['year_v'] = year_v
        context['username'] = UserAccessProfile(self.request).username  # the_user(self.request)
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def getTotalMonthUsage(any_day):
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)
    return Reservation.objects.filter(status__in=[3, 4],
                                      start_time__gte=curr_start,
                                      end_time__lte=curr_end).count()


def getTotalLastYear(any_day):
    month_list = []
    value_list = []
    for i in range(0, 12):
        gday = any_day + relativedelta(months=-i)
        month_list.insert(0, gday.strftime('%B'))
        value_list.insert(0, getTotalMonthUsage(gday))
    return month_list, value_list


def getMonthUsage(user_ref, any_day):
    curr_start = any_day.replace(day=1).replace(hour=0, minute=0, second=0)
    curr_end = last_day_of_month(any_day).replace(hour=23, minute=59, second=59)
    return Reservation.objects.filter(user_ref=user_ref,
                                      status__in=[3, 4],
                                      start_time__gte=curr_start,
                                      end_time__lte=curr_end).count()


def getLastYear(user_ref, any_day):
    month_list = []
    value_list = []
    for i in range(0, 12):
        gday = any_day + relativedelta(months=-i)
        month_list.insert(0, gday.strftime('%B'))
        value_list.insert(0, getMonthUsage(user_ref, gday))

    # month_list = ast.literal_eval(month_list.pop())
    return month_list, value_list
