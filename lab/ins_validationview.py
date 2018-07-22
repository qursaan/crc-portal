
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from portal.actions import get_user_by_email, get_user_type
from lab.actions import get_std_requests
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # the_user,
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class ValidatePendingView(LoginRequiredAutoLogoutView):
    def get(self, request):
        page = Page(self.request)
        usera = UserAccessProfile(request)
        c_user = usera.user_obj #get_user_by_email(the_user(self.request))
        user_type = usera.user_type #get_user_type(c_user)
        if user_type != 2:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "ins-validate-view.html"

        std_requests = get_std_requests(c_user.id)

        template_env = {
            'topmenu_items': topmenu_items('Validation', page.request),
            # 'errors': errors,
            'username': usera.username,
            'std_pending_list': std_requests,
            'title': 'Manage Student',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)




