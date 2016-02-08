__author__ = 'pirate'

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from dateutil import parser
from unfold.page import Page
from portal.models import SimReservation, VirtualNode, SimulationVM, ReservationDetail
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu import topmenu_items, the_user


class SchedulerView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        self.user_email = the_user(request)
        page = Page(request)

        server_type = "omf"
        request_date = timezone.now()
        node_list = []
        reserve_list = []

        if request.POST: # method == 'POST':
            self.errors = []
            request_date = request.POST.get('request_date', timezone.now())
            server_type = request.POST.get('server_type', 'omf')
            request_date = parser.parse(request_date)

        # Resources
        # resources_list = VirtualNode.objects.all()
        day_start = request_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        if server_type == "omf":
            node_list = VirtualNode.objects.all()
            reserve_list = ReservationDetail.objects.filter(reservation_ref__status=3,
                                                            reservation_ref__start_time__gte=day_start) #,
                                                            #reservation_ref__end_time__lt=day_end)
           # for r in reserve_list:
            #    if r.reservation_ref.end_time > day_end:
            #        r.reservation_ref.end_time = day_end

        elif server_type == "sim":
            node_list = SimulationVM.objects.all()
            reserve_list = SimReservation.objects.filter(status=3,
                                                         start_time__gte=day_start) #,
                                                        # end_time__lt=day_end)

        template_env = {
            'topmenu_items': topmenu_items('Scheduler View', page.request),
            'username': the_user(request),
            'server_type': request.POST.get('server_type', server_type),
            'errors': self.errors,
            'title': "Scheduler View",
            'request_date': request_date,
            'node_list': node_list,
            'reserve_list': reserve_list,
        }
        template_env.update(page.prelude_env())
        return render(request, 'scheduler-view.html', template_env)
