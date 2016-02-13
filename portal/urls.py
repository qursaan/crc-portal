from django.views.generic.base import TemplateView
# from django.views.generic      import TemplateView
# from django.views              import generic
from django.conf.urls import url  # patterns

from portal.homeview import HomeView
from portal.registrationview import RegistrationView
from portal.accountview import AccountView, account_process
from portal.supportview import SupportView
from portal.contactview import ContactView
from portal.dashboardview import DashboardView
from portal.validationview import ValidatePendingView

from portal.slicependingview import SliceCurrentView, SliceHistoryView,\
    slice_o_pending_process, slice_s_pending_process, \
    slice_o_pending_cancel, slice_s_pending_cancel

from portal.slicecontrolview import SliceControlView, \
    control_load_image, control_save_image, \
    control_check_load, control_check_save, \
    control_load_sample, control_remote_node, \
    control_exe_script, control_check_exe, control_exe_abort

from portal.sliceview import SliceView
from portal.testbedview import TestbedView, check_status
from portal.schedulerview import SchedulerView, check_scheduler
from portal.documentationview import DocumentationView
from portal.experimentview import ExperimentView
from portal.navigation import *
from portal.filemanagerview import FileManagerView
from portal.graphicview import GraphicBuilderView
from portal.reservationview import ReservationView, check_availability

#
#

urlpatterns = [
    url(r'^access/?$', HomeView.as_view(), name='access'),

    # User registration
    url(r'^register/?$', RegistrationView.as_view(), name='registration'),
    url(r'^user/register/complete/$',
        TemplateView.as_view(template_name='user_register_complete.html'),
        name='user_register_complete'),

    # password management
    url(r'^pass_reset/$', 'portal.django_passresetview.password_reset',
        {'post_reset_redirect': '/portal/password/reset/done/'}),
    url(r'^password/reset/done/$', 'portal.django_passresetview.password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'portal.django_passresetview.password_reset_confirm',
        {'post_reset_redirect': '/portal/password/done/'}),
    url(r'^password/done/$', 'portal.django_passresetview.password_reset_complete'),

    # Profile
    url(r'^account/?$', AccountView.as_view(), name='account'),
    url(r'^account/account_process/?$', account_process),

    # Support and Contacts
    url(r'^contact/?$', ContactView.as_view(), name='contact'),
    url(r'^support/?$', SupportView.as_view(), name='support'),
    url(r'^support/documentation/?$', DocumentationView.as_view(), name='FAQ'),
    url(r'^experiment?$', ExperimentView.as_view(), name='experiment'),

    # Validate pending requests
    url(r'^validate/?$', ValidatePendingView.as_view()),
    url(r'^validate_action(?P<id>(?:/\w+)+)/?$', 'portal.actions.validate_action'),

    # Log and History
    url(r'^history/?$', un_complete_page),

    # Dashboard
    url(r'^dashboard/?$', DashboardView.as_view(), {'state': 'Welcome to CRC'}),

    # Testbeds
    url(r'^testbeds/map/?$', TestbedView.as_view(), name="testbeds"),
    url(r'^testbeds/map/check_status?$', check_status),
    # url(r'^testbeds/timeline/?$', TimelineView.as_view(), name='Timeline'),
    url(r'^testbeds/scheduler/?$', SchedulerView.as_view(), name='Scheduler'),
    url(r'^testbeds/scheduler/check_scheduler?$', check_scheduler),
    url(r'^testbeds/slice/?$', SliceView.as_view(), name='slice'),

    # Tools
    url(r'^lab/tools/builder/?$', GraphicBuilderView.as_view(), name="g_builder"),
    url(r'^lab/tools/file_manager/?$', FileManagerView.as_view(), name="file_manager"),

    # Reservation
    url(r'^lab/current/?$', SliceCurrentView.as_view(), name="slice_pending"),
    url(r'^lab/current/slice_o_process/(\d{1,10})/?$', slice_o_pending_process),
    url(r'^lab/current/slice_s_process/(\d{1,10})/?$', slice_s_pending_process),
    url(r'^lab/current/slice_o_cancel/(\d{1,10})/?$', slice_o_pending_cancel),
    url(r'^lab/current/slice_s_cancel/(\d{1,10})/?$', slice_s_pending_cancel),
    url(r'^lab/control/?$', SliceControlView.as_view(), name="slice_control"),
    url(r'^lab/control/control_load_image/?$', control_load_image),
    url(r'^lab/control/control_save_image/?$', control_save_image),
    url(r'^lab/control/control_check_load/?$', control_check_load),
    url(r'^lab/control/control_check_save/?$', control_check_save),
    url(r'^lab/control/control_check_exe/?$', control_check_exe),
    url(r'^lab/control/control_exe_script/?$', control_exe_script),
    url(r'^lab/control/control_exe_abort/?$', control_exe_abort),
    url(r'^lab/control/control_remote_node?$', control_remote_node),
    url(r'^lab/control/load_samples?$', control_load_sample),
    url(r'^lab/history/?$', SliceHistoryView.as_view(), name="slice_history"),
    # url(r'^lab/slice_request/?$', SliceRequestView.as_view(), name='slice_request'),
    url(r'^lab/reservation/?$', ReservationView.as_view(), name='Reservation'),
    url(r'^lab/reservation/check_availability?$', check_availability),


    # Others
    url(r'/?$', un_complete_page),
    # url(r'^reservation/new/?$', uncomplete),

]
