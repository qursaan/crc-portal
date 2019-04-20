from lab.actions import get_count_students_course, \
    get_count_students_pending, \
    get_count_bulk_experiments, \
    get_count_students_experiments, \
    get_count_students
from portal.actions import get_count_active_slice, get_count_requests
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# This view requires login
class DashboardView(LoginRequiredAutoLogoutView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        # We might have slices on different registries with different user accounts 
        # We note that this portal could be specific to a given registry, to which we register users, but i'm not sure that simplifies things
        # Different registries mean different identities, unless we identify via SFA HRN or have associated the user email to a single hrn

        # messages.info(self.request, 'You have logged in')
        page = Page(self.request)
        # the page header and other stuff
        usera = UserAccessProfile(self.request)
        # c_user_email =  the_user(self.request)
        c_user = usera.user_obj # get_user_by_email(c_user_email)
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['username'] = usera.username
        context['topmenu_items'] = topmenu_items('Dashboard', page.request)
        context['active_count'] = get_count_active_slice(c_user,usera.session_username)
        context['course_count'] = get_count_students_course(c_user)
        context['pending_count'] = get_count_students_pending(c_user)
        context['std_exp_count'] = get_count_students_experiments(c_user)
        context['student_count'] = get_count_students(c_user)
        context['request_count'] = get_count_requests() if usera.user_type == 0 else 0
        context['bulk_count'] = get_count_bulk_experiments(c_user)
        context['user_type'] = usera.user_type
        context.update(page.prelude_env())
        return context
