# from random import randint

# from django.contrib.auth        import get_user_model
# from django.contrib.auth.models import User
# from django.core.mail           import send_mail
from django.shortcuts import render

# @qursaan
from portal.forms import CaptchaTestForm
from portal.modules import *
# from crc.settings               import SUPPORT_EMAIL
from unfold.loginrequired import FreeAccessView
from unfold.page import Page


# from django.template.loader     import render_to_string


# @qursaan: comment
# from manifold.manifoldapi       import execute_admin_query
# from manifold.core.query        import Query
# from portal.actions import authority_get_pi_emails, manifold_add_user, manifold_add_account


class RegistrationView(FreeAccessView):

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        errors = []

        # @qursaan: get authorities from db
        authorities = Authority.objects.all()
        if authorities is not None:
            authorities = sorted(authorities)

        # get all supervisors
        supervisors = MyUser.objects.filter(user_type=2)

        # get all quotas
        quotas = Quota.objects.all()

        # @qursaan: change to user table
        # user_details = User.objects.all()  # execute_admin_query(self.request, user_query)

        page = Page(request)
        page.add_js_files(["js/jquery-1.11.1.js", "js/my_account.register.js", ])
        page.add_css_files(["css/registration.css", ])

        if method == 'POST':
            # @qursaan: get post values
            # get_email = PendingUser.objects.get(email)
            reg_fname = request.POST.get('firstname', '')
            reg_lname = request.POST.get('lastname', '')
            reg_auth = request.POST.get('authority_hrn', '')
            reg_username = request.POST.get('username', '').lower()
            reg_email = request.POST.get('email', '').lower()
            reg_password = request.POST.get('password', '')  # request.POST['password']
            reg_usertype = request.POST.get('usertype', '')
            reg_supervisor = request.POST.get('supervisor', '')
            reg_quota = request.POST.get('quota', '')

            form = CaptchaTestForm(request.POST)
            if not form.is_valid():
                errors.append('Invalid Captcha')

            if not errors:
                errors = UserModules.create_user_account(errors, reg_email, reg_username, reg_password,
                                                         reg_fname, reg_lname, reg_auth, reg_usertype,
                                                         reg_supervisor, reg_quota)

            if not errors:
                return render(request, 'user_register_complete.html')
        ###################################################################

        # Error or Get
        template_env = {
            #'topmenu_items': topmenu_items('Register', page.request),
            'errors': errors,
            'firstname': request.POST.get('firstname', ''),
            'lastname': request.POST.get('lastname', ''),
            'username': request.POST.get('username', ''),
            'authority_hrn': request.POST.get('authority_hrn', ''),
            'email': request.POST.get('email', ''),
            'password': request.POST.get('password', ''),
            'usertype': request.POST.get('usertype', ''),
            'authorities': authorities,
            'supervisors': supervisors,
            'quotas': quotas,
            'title': 'Registration',
            'form': CaptchaTestForm(),
        }
        template_env.update(page.prelude_env())
        return render(request, 'registration-view.html', template_env)
