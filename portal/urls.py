from django.views.generic.base import TemplateView
#from django.views.generic      import TemplateView
#from django.views              import generic
from django.conf.urls           import url, include #patterns

from portal.homeview            import HomeView
from portal.registrationview    import RegistrationView
from portal.accountview         import AccountView, account_process
from portal.supportview         import SupportView
from portal.contactview         import ContactView
from portal.dashboardview       import DashboardView
from portal.validationview      import ValidatePendingView
from portal.slicerequestview    import SliceRequestView
from portal.slicependingview    import SlicePindingView, SliceHistoryView, slice_pending_process,slice_pending_cancel
from portal.slicecontrolview    import SliceControlView, control_load_image, control_save_image, control_exe_script, control_load_sample, control_remote_node
from portal.sliceview           import SliceView
from portal.testbedview         import TestbedView, check_status
from portal.schedulerview       import SchedulerView
from portal.documentationview   import DocumentationView
from portal.experimentview      import ExperimentView
from portal.navigation          import *
from portal.filemanagerview     import FileManagerView
from portal.graphicview         import GraphicBuilderView
from portal.reservationview     import ReservationView

#
#
from portal.django_passresetview import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from portal.navigation import load_image

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
    #url(r'^testbeds/timeline/?$', TimelineView.as_view(), name='Timeline'),
    url(r'^testbeds/scheduler/?$', SchedulerView.as_view(), name='Scheduler'),
    url(r'^testbeds/slice/?$', SliceView.as_view(), name='slice'),

    # Tools
    url(r'^lab/tools/builder/?$', GraphicBuilderView.as_view(), name="g_builder"),
    url(r'^lab/tools/file_manager/?$', FileManagerView.as_view(), name="file_manager"),

    # Reservation
    url(r'^lab/current/?$', SlicePindingView.as_view(), name="slice_pending"),
    url(r'^lab/current/slice_process/(\d{1,10})/?$', slice_pending_process),
    url(r'^lab/current/slice_cancel/(\d{1,10})/?$', slice_pending_cancel),
    url(r'^lab/control/?$', SliceControlView.as_view(), name="slice_control"),
    url(r'^lab/control/control_load_image/?$', control_load_image),
    url(r'^lab/control/control_save_image/?$', control_save_image),
    url(r'^lab/control/control_exe_script/?$', control_exe_script),
    #url(r'^lab/control/create_exe_post?$', create_exe_post),
    url(r'^lab/control/control_remote_node?$', control_remote_node),
    url(r'^lab/control/load_samples?$', control_load_sample),
    url(r'^lab/history/?$', SliceHistoryView.as_view(), name="slice_history"),
    url(r'^lab/slice_request/?$', SliceRequestView.as_view(), name='slice_request'),
    url(r'^lab/reservation/?$', ReservationView.as_view(), name='Reservation'),

    # Others
    url(r'/?$', un_complete_page),
    # url(r'^reservation/new/?$', uncomplete),

]
