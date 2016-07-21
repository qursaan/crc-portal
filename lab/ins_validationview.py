

from django.contrib import messages
from django.shortcuts import render
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page

from ui.topmenu import the_user, topmenu_items
from django.http import HttpResponseRedirect
from portal.actions import get_user_by_email, get_user_type
from lab.actions import get_std_requests


class ValidatePendingView(LoginRequiredAutoLogoutView):
    def get(self, request):
        page = Page(self.request)

        c_user = get_user_by_email(the_user(self.request))
        user_type = get_user_type(c_user)
        if user_type != 2:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "ins-validate-view.html"

        std_requests = get_std_requests(c_user.id)

        template_env = {
            'topmenu_items': topmenu_items('Validation', page.request),
            # 'errors': errors,
            'username': the_user(self.request),
            'std_pending_list': std_requests,
            'title': 'Manage Student',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)




