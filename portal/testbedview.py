__author__ = 'pirate'
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from portal.backend_actions import get_vm_status
from portal.models import VirtualNode, PhysicalNode
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page

from portal.models import ReservationDetail, Reservation
from howdy.models import Variable,output
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu import topmenu_items, the_user
from datetime import datetime
from django.utils import timezone

# ********** View Testbed Map Page *********** #
class TestbedView(LoginRequiredAutoLogoutView):
    template_name = "testbed-view.html"

    def dispatch(self, *args, **kwargs):
        # if 'to_upload' in self.request.POST:
        # print(self.request.POST)
        # print(self.request.POST.get('upload_nodes'))
        if self.request.POST.get('upload_nodes'):
            # print(self.request.method)
            self.request.session['node_id'] = self.request.POST.get('upload_nodes')
            # print(self.request.session['node_id'])
            return HttpResponseRedirect('/portal/upload/')
        # elif 'to_vars' in self.request.POST:

        elif self.request.POST.get('var_name'):
            self.request.session['vars'] = self.request.POST.get('var_name')
            # print(self.request.session['var_name'])
            return HttpResponseRedirect('/portal/Manage_Varaibles/')

        elif self.request.POST.get('node_id_for_vars'):
            device = self.request.POST.get('upload_nodes')
            self.request.session['node_id_for_vars_session'] = self.request.POST.get('node_id_for_vars')
            # self.request.session['user_id_for_vars_session'] =user.id
            # print(self.request.session['var_name'])
            return HttpResponseRedirect('/portal/Manage_Varaibles_user/')
        elif self.request.POST.get('submit_LEds'):
            print('------------------submit_LEds------------------------')
            device = self.request.POST.get('submit_LEds')
            LED1values = self.request.POST.get('LED1')
            LED2values = self.request.POST.get('LED2')
            __deviceID_id = self.request.POST.get('submit_LEds')
            print('-----------------------------------------------------')
            print(LED1values)
            print(LED2values)
            print(__deviceID_id)

            NodeLED = output.objects.filter(deviceID_id=__deviceID_id, outputName='LED1')
            print(NodeLED)
            NodeLED.update(value=[1, 0][LED1values != '1'])

            NodeLED2 = output.objects.filter(deviceID_id=__deviceID_id, outputName='LED2')
            print(NodeLED2)
            NodeLED2.update(value=[1, 0][LED2values != '1'])

            print('-----------------------------------------------------')
            return HttpResponseRedirect('/portal/testbeds/map/')
        return super(TestbedView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        usera = UserAccessProfile(self.request)
        user = usera.user_obj  # get_user_by_email(user_hrn)

        active_reservations = Reservation.objects.filter(user_ref=user, f_start_time__lte=timezone.now(),
                                                         f_end_time__gt=timezone.now())
        print(active_reservations.values_list('f_start_time'))

        reservations_detail = ReservationDetail.objects.filter(reservation_ref=active_reservations).values_list(
            'node_ref_id')
        virtualnodes = VirtualNode.objects.filter(pk__in=reservations_detail).values_list('node_ref_id')

        # print (virtualnodes)
        # virtualnodes = VirtualNode(reservations_detail.select_related('node_ref')).objects.all()

        # print (virtualnodes[0])

        node_list = PhysicalNode.objects.filter(pk__in=virtualnodes)  # all()#

        # node_list = virtualnodes.prefetch_related('node_ref')

        print(node_list.values_list('id'))

        vm_list = VirtualNode.objects.all().order_by('node_ref')
        #node_list = PhysicalNode.objects.all()
        var_list = Variable.objects.filter(usernameID=user).order_by('deviceID_id')
        context = super(TestbedView, self).get_context_data(**kwargs)
        context['vm_list'] = vm_list
        context['var_list'] = var_list
        #context['node_list'] = node_list
        context['last_update'] = datetime.now()
        context['title'] = 'TESTBEDS VIEW'
        context['username'] = UserAccessProfile(self.request).username
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def check_status(request):
    if "upload_nodes" in request.POST:
        n_id = request.POST.get('upload_nodes')
        # ol = get_vm_status(n_id)
        print(request.POST.get(
            'upload_nodes'))  # return HttpResponse(ol, content_type="application/json")  # else:  # return HttpResponse('{"Error": "Error"}', content_type="application/json")
    '''
    
    if "the_post" in request.POST:
        n_id = request.POST.get('the_post')
        ol = get_vm_status(n_id)
        return HttpResponse(ol, content_type="application/json")
    else:
        return HttpResponse('{"Error": "Error"}', content_type="application/json")
    
    '''