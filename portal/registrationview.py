import os.path, re
import json
from random import randint

from django.core.mail           import send_mail
from django.contrib.auth.models import User

from django.template.loader     import render_to_string
from django.shortcuts           import render
from django.contrib.auth        import get_user_model

from unfold.page                import Page
from unfold.loginrequired       import FreeAccessView
from ui.topmenu                 import topmenu_items
#
from crc.settings               import SUPPORT_EMAIL

# @qursaan: comment
#from manifold.manifoldapi       import execute_admin_query
#from manifold.core.query        import Query

from portal.models              import PendingUser, MyUser, Account, Platform
#from portal.actions             import authority_get_pi_emails, manifold_add_user, manifold_add_account

# @qursaan
from portal.models import Authority


class RegistrationView (FreeAccessView):

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        errors = []

        # @qursaan: comment not needed
        # Using cache manifold-tables to get the list of authorities faster
        # authorities_query = Query.get('portal_authority').select('name', 'authority_hrn')
        # authorities = execute_admin_query(request, authorities_query)

        # @qursaan: get authorities from db
        authorities = Authority.objects.all()

        if authorities is not None:
            authorities = sorted(authorities)

        # xxx tocheck - if authorities is empty, it's no use anyway
        # (users won't be able to validate the form anyway)

        page = Page(request)
        page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", ])
        page.add_css_files(["css/onelab.css", "css/registration.css", ])
        page.add_css_files(["http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css", ])

        print 'registration view, method', method

        #user_query  = Query().get('local:user').select('user_id', 'email')
        # @qursaan: change to user table
        user_details = User.objects.all()  # execute_admin_query(self.request, user_query)

        if method == 'POST':
            # @qursaan: get values
            #get_email = PendingUser.objects.get(email)
            reg_fname  = request.POST.get('firstname', '')
            reg_lname  = request.POST.get('lastname', '')
            reg_auth   = request.POST.get('authority_hrn', '')
            #reg_login  = request.POST.get('login', '')
            reg_email  = request.POST.get('email','').lower()
            #prepare user_hrn
            split_email = reg_email.split("@")[0]
            split_email = split_email.replace(".", "_")
            user_hrn = reg_auth + '.' + split_email+ str(randint(1, 1000000))
            print "User_Hrn: ", user_hrn
            UserModel = get_user_model()

            #POST value validation
            if (re.search(r'^[\w+\s.@+-]+$', reg_fname)==None):
                errors.append('First Name may contain only letters, numbers, spaces and @/./+/-/_ characters.')
            if (re.search(r'^[\w+\s.@+-]+$', reg_lname)==None):
                errors.append('Last Name may contain only letters, numbers, spaces and @/./+/-/_ characters.')


            # checking in django_db !!

            if MyUser.objects.filter(email__iexact=reg_email, status=1):
                errors.append('Email is pending for validation. Please provide a new email address.')
            elif MyUser.objects.filter(email__iexact=reg_email, status=0):
                errors.append('This account is disabled. Please contact the administrator')
            #if PendingUser.objects.filter(email__iexact=reg_email):
            #    errors.append('Email is pending for validation. Please provide a new email address.')
            elif UserModel._default_manager.filter(email__iexact=reg_email):
                errors.append('This email is not usable. Please contact the administrator or try with another email.')
            else:
                for user_detail in user_details:
                    if user_detail.email == reg_email: #@qursaan change user_detail['email']
                        errors.append('Email already registered in CRC Server. Please provide a new email address.')
                        break

            ##################################################
            # XXX TODO: Factorize with portal/accountview.py
            # @qursaan: set auto generation
            if not errors:  # 'generate' in request.POST['question']:
                from Crypto.PublicKey import RSA
                private = RSA.generate(1024)
                private_key = json.dumps(private.exportKey())
                public = private.publickey()
                public_key = json.dumps(public.exportKey(format='OpenSSH'))

                # Saving to DB
                account_config = '{"user_public_key":' + public_key + \
                                 ', "user_private_key":' + private_key + \
                                 ', "user_hrn":"' + user_hrn + '"}'
                auth_type = 'managed'

                # for sending email: removing existing double qoute
                public_key = public_key.replace('"', '');
            """
            else:  # @qursaan: user upload a key
                up_file = request.FILES['user_public_key']
                file_content = up_file.read()
                file_name = up_file.name
                file_extension = os.path.splitext(file_name)[1]
                allowed_extension = ['.pub','.txt']
                if file_extension in allowed_extension and re.search(r'ssh-rsa',file_content):
                    account_config = '{"user_public_key":"'+ file_content + '", "user_hrn":"' + user_hrn + '"}'
                    account_config = re.sub("\r", "", account_config)
                    account_config = re.sub("\n", "\\n",account_config)
                    account_config = ''.join(account_config.split())
                    auth_type = 'user'
                    # for sending email
                    public_key = file_content
                    public_key = ''.join(public_key.split())
                else:
                    errors.append('Please upload a valid RSA public key.')
            """
            ###################################################################


            #saving to django db 'portal_pendinguser' table
            if not errors:
                # @qursaan: PendingUser -> MyUser
                """pnd_user = PendingUser(
                    first_name    = reg_fname,
                    last_name     = reg_lname,
                    authority_hrn = reg_auth,
                    #login        = reg_login,
                    email         = reg_email,
                    password      = request.POST['password'],
                    keypair       = account_config,
                    user_hrn      = user_hrn,
                )
                pnd_user.save()"""
                # saves the user to django auth_user table [needed for password reset]
                web_user = User.objects.create_user(reg_email, reg_email, request.POST['password'])
                # @qursaan: set user inactive
                web_user.first_name = reg_fname
                web_user.last_name = reg_lname
                web_user.is_active = False
                web_user.save()
                # creating user to manifold local:user
                # @qursaan: comments
                # user_config = '{"firstname":"' + reg_fname + \
                #              '", "lastname":"' + reg_lname + \
                #              '", "authority":"' + reg_auth + '"}'
                # user_params = {'email': reg_email,
                #               'password': request.POST['password'],
                #               'config': user_config,
                #               'status': 1}
                # manifold_add_user(request, user_params)

                # @qursaan: add create user to backend
                itf_user = MyUser(
                    first_name    = reg_fname,
                    last_name     = reg_lname,
                    authority_hrn = reg_auth,
                    #login        = reg_login,
                    email         = reg_email,
                    password      = request.POST['password'],
                    keypair       = account_config,
                    user_hrn      = user_hrn,
                    status        = 1,  # set 1 = Pending
                )
                itf_user.id = web_user.id
                itf_user.save()

                # creating local:account in manifold
                # @qursaan: comments
                # user_id = user_detail.id + 1 # the user_id for the newly created user in local:user
                # account_params = {'platform_id': 5,
                #                  'user_id': user_id,
                #                  'auth_type': auth_type,
                #                  'config': account_config}
                # manifold_add_account(request, account_params)
                itf_plf = Platform.objects.get(id=1)
                itf_acc = Account(
                    user_ref     = itf_user,
                    platform_ref = itf_plf,
                    auth_type    = auth_type,
                    config       = account_config,
                )
                itf_acc.save()

                # print "USER ID:", user_id

                # Send email
                ctx = {
                    'first_name'    : reg_fname,
                    'last_name'     : reg_lname,
                    'authority_hrn' : reg_auth,
                    'email'         : reg_email,
                    'user_hrn'      : user_hrn,
                    'public_key'    : public_key,
                    }
                # @qursaan: send to authority only
                auth_email = Authority.objects.get(authority_hrn=reg_auth)
                recipients = [auth_email.email]
                #recipients = authority_get_pi_emails(request, reg_auth)
                # backup email: if authority_get_pi_emails fails
                recipients.append(SUPPORT_EMAIL)

                msg = render_to_string('user_request_email.txt', ctx)
                send_mail("CRC New User request for %s submitted"%reg_email,
                          msg, 'qursaan@crclab.org', recipients)
                return render(request, 'user_register_complete.html')

        # Error or Get
        template_env = {
            'topmenu_items': topmenu_items('Register', page.request),
            'errors': errors,
            'firstname': request.POST.get('firstname', ''),
            'lastname': request.POST.get('lastname', ''),
            'authority_hrn': request.POST.get('authority_hrn', ''),
            'email': request.POST.get('email', ''),
            'password': request.POST.get('password', ''),
            'authorities': authorities,
            'title': 'Registration',
          }
        template_env.update(page.prelude_env())
        return render(request, 'registration_view.html', template_env)
