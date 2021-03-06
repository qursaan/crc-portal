__author__ = 'pirate'

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
#
from django.utils import timezone

from portal.actions import get_count_active_slice
from portal.models import Reservation, SimReservation
from portal.reservation_status import ReservationStatus
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
#
from unfold.page import Page
from crc.settings import SIM_RESERVATION

# status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
class SliceHistoryView(LoginRequiredAutoLogoutView):
    template_name = "slicehistory-view.html"

    def dispatch(self, *args, **kwargs):
        return super(SliceHistoryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", "js/my_account.edit_profile.js"])
        page.add_css_files(["css/plugin.css"])

        usera = UserAccessProfile(self.request)

        c_user = usera.user_obj #get_user_by_email(the_user(self.request))
        history_list_omf = Reservation.objects.filter(user_ref=c_user,username=usera.session_username)
        history_list_sim = SimReservation.objects.filter(user_ref=c_user,username=usera.session_username)
        context = super(SliceHistoryView, self).get_context_data(**kwargs)
        context['history_list_omf'] = history_list_omf
        context['history_list_sim'] = history_list_sim
        context['time_now'] = timezone.now
        context['title'] = 'Request Log'
        context['sim_enable'] = SIM_RESERVATION
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('Request Log', page.request)  # @qursaan change from _live
        # so we can sho who is logged
        context['username'] = usera.username #the_user(self.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


class SliceCurrentView(LoginRequiredAutoLogoutView):
    template_name = "slicepending-view.html"

    def dispatch(self, *args, **kwargs):
        return super(SliceCurrentView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", "js/my_account.edit_profile.js"])
        page.add_css_files(["css/plugin.css"])
        usera = UserAccessProfile(self.request)
        c_user = usera.user_obj # get_user_by_email(the_user(self.request))
        get_count_active_slice(c_user=c_user,username=usera.session_username)
        pending_list_1 = Reservation.objects.filter(user_ref=c_user,username=usera.session_username, status=ReservationStatus.get_pending())
        active_list_1 = Reservation.objects.filter(user_ref=c_user,username=usera.session_username, status=ReservationStatus.get_active())
        pending_list_2 = SimReservation.objects.filter(user_ref=c_user,username=usera.session_username, status=ReservationStatus.get_pending())
        active_list_2 = SimReservation.objects.filter(user_ref=c_user,username=usera.session_username, status=ReservationStatus.get_active())

        context = super(SliceCurrentView, self).get_context_data(**kwargs)
        context['current_list_1'] = pending_list_1
        context['active_list_1'] = active_list_1
        context['current_list_2'] = pending_list_2
        context['active_list_2'] = active_list_2

        context['time_now'] = timezone.now()
        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Reservation Panel'
        # the menu items on the top
        # context['topmenu_items'] = topmenu_items('Reservation Status', page.request)  # @qursaan change from _live
        # so we can sho who is logged
        context['username'] = usera.username # the_user(self.request)
        # context ['firstname'] = config['firstname']
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def slice_o_pending_process(request, slice_id):
    return slice_pending_process(request,slice_id,"omf")


@login_required
def slice_s_pending_process(request, slice_id):
    return slice_pending_process(request,slice_id,"sim")


@login_required
def slice_pending_process(request, slice_id, stype):
    slice_id = int(slice_id)
    current_slice = None

    if stype == "sim":
        current_slice = SimReservation.objects.get(id=slice_id)
    elif stype == "omf":
        current_slice = Reservation.objects.get(id=slice_id)

    if current_slice is None or current_slice.status != ReservationStatus.get_active():
        messages.success(request, 'Error: You have not permission to access this page.')
        return HttpResponseRedirect("/portal/lab/current/")
    if current_slice.end_time < timezone.now():
        current_slice.status = ReservationStatus.get_expired()
        current_slice.save()
        messages.success(request, 'Error: Slice time has been expired. ')
        return HttpResponseRedirect("/portal/lab/current/")

    request.session['slice_id'] = slice_id
    request.session['stype'] = stype
    return HttpResponseRedirect("/portal/lab/control/")


@login_required
def slice_o_pending_cancel(request, slice_id):
    slice_id = int(slice_id)
    current_slice = Reservation.objects.get(id=slice_id)
    current_slice.status = ReservationStatus.get_canceled()
    current_slice.save()
    messages.success(request, 'Success: Cancel Slice.')
    return HttpResponseRedirect("/portal/lab/current/")


@login_required
def slice_s_pending_cancel(request, slice_id):
    slice_id = int(slice_id)
    current_slice = SimReservation.objects.get(id=slice_id)
    current_slice.status = ReservationStatus.get_canceled()
    current_slice.save()
    messages.success(request, 'Success: Cancel Slice.')
    return HttpResponseRedirect("/portal/lab/current/")