from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from portal.user_access_profile import UserAccessProfile
# from portal.actions import get_user_by_email
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


#
# from manifold.core.query import Query
# from manifold.manifoldapi  mport execute_query
# from portal.actions import manifold_update_user, manifold_update_account, manifold_add_account, manifold_delete_account, sfa_update_user
# from django.core.mail import send_mail

# requires login


class AccountView(LoginRequiredAutoLogoutView):
    template_name = "account-view.html"

    def dispatch(self, *args, **kwargs):
        return super(AccountView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        page = Page(self.request)
        page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", "js/my_account.edit_profile.js"])
        page.add_css_files(["css/account_view.css", "css/plugin.css"])

        # @qursaan
        # user_details = MyUser.objects.filter(email=the_user(self.request))
        # user_query  = Query().get('local:user').select('config','email','status')
        # user_details = execute_query(self.request, user_query)
        usera = UserAccessProfile(self.request)
        user_detail = usera.user_obj  # get_user_by_email(the_user(self.request))

        # not always found in user_details...
        config = {}
        user_status = 'N/A'
        user_fname = '?'
        user_lname = '?'
        user_authu = 'Unknown Authority'
        user_ID = '_'

        # for user_detail in user_details:
        if user_detail:
            # different significations of user_status
            if user_detail.status == 0:
                user_status = 'Disabled'
            elif user_detail.status == 1:
                user_status = 'Validation Pending'
            elif user_detail.status == 2:
                user_status = 'Enabled'
            else:
                user_status = 'N/A'

            user_fname = user_detail.first_name
            user_lname = user_detail.last_name
            user_authu = user_detail.authority_hrn
            user_ID = user_detail.id

        context = super(AccountView, self).get_context_data(**kwargs)
        # context['principal_acc'] = principal_acc_list
        # context['ref_acc'] = ref_acc_list
        # context['platform_list'] = platform_list
        # context['my_users'] = my_users
        # context['my_slices'] = my_slices
        # context['my_auths'] = my_auths
        context['id'] = user_ID
        context['user_status'] = user_status
        context['person'] = self.request.user
        context['firstname'] = user_fname  # config.get('firstname',"?")
        context['lastname'] = user_lname  # config.get('lastname',"?")
        context['fullname'] = context['firstname'] + ' ' + context['lastname']
        context['authority'] = user_authu  # config.get('authority',"Unknown Authority")
        # context['user_private_key'] = account_priv_key
        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Account Information'
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('My Account', page.request)  # @qursaan change from _live
        # so we can sho who is logged
        context['username'] = usera.username
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


# my_acc form value processing
@login_required
def account_process(request):
    user_id = ''
    usera = UserAccessProfile(request)
    user_details = usera.user_obj  # get_user_by_email(the_user(request))
    if user_details:
        user_id = user_details.id

    if 'submit_name' in request.POST:
        # edited_first_name = request.POST['fname']
        # edited_last_name = request.POST['lname']

        # config={}
        # for user_config in user_details:
        #    if user_config['config']:
        #        config = json.loads(user_config['config'])
        #        config['firstname'] = edited_first_name
        #        config['lastname'] = edited_last_name
        #        config['authority'] = config.get('authority','Unknown Authority')
        # updated_config = json.dumps(config)
        # user_params = {'config': updated_config}
        #    else: # it's needed if the config is empty
        #        user_config['config']= '{"firstname":"' + edited_first_name + '", "lastname":"'+ edited_last_name + '", "authority": "Unknown Authority"}'
        #        #user_params = {'config': user_config['config']}
        # updating config local:user in manifold       
        # manifold_update_user(request, request.user.email,user_params)

        # this will be depricated, we will show the success msg in same page
        # Redirect to same page with success message
        if user_details:
            user_details.first_name = request.POST['fname']
            user_details.last_name = request.POST['lname']
            user_details.save()
            messages.success(request, 'Success: First Name and Last Name Updated.')
        else:
            messages.error(request, 'Error: User not found, Try again')
        return HttpResponseRedirect("/portal/account/")

    elif 'submit_pass' in request.POST:
        # edited_password = request.POST['password']

        # for user_pass in user_details:
        #    user_pass['password'] = edited_password
        # updating password in local:user
        # user_params = { 'password': user_pass['password']}
        # manifold_update_user(request,request.user.email,user_params)
        #        return HttpResponse('Success: Password Changed!!')
        if user_details:
            web_user = User.objects.get_by_natural_key(usera.username)
            # TODO: change web user password
            user_details.password = request.POST['password']
            messages.success(request, 'Success: Password Updated.')
        else:
            messages.error(request, 'Error: User not found, Try again')
        return HttpResponseRedirect("/portal/account/")

    else:
        messages.info(request, 'Under Construction. Please try again later!')
        return HttpResponseRedirect("/portal/account/")
