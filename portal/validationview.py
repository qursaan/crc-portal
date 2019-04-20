from portal.actions import get_requests  # , get_user_by_email
from portal.models import Authority
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView  # ,FreeAccessView
from unfold.page import Page


class ValidatePendingView(LoginRequiredAutoLogoutView):  # FreeAccessView):
    template_name = "validate_pending.html"

    def get_context_data(self, **kwargs):
        # messages.info(self.request, 'You have logged in')
        page = Page(self.request)
        ctx_my_authorities = {}
        # The user need to be logged in
        usera = UserAccessProfile(self.request)
        if usera.username:
            user = usera.user_obj  # get_user_by_email(u_email=the_user(page.request))
            pi_authorities_tmp = Authority.objects.filter(authority_hrn=user.authority_hrn).all()
            pi_authorities = set()
            for pa in pi_authorities_tmp:
                # pi_authorities |= set(pa.authority_hrn) #['pi_authorities'])
                pi_authorities = pi_authorities.union([user.authority_hrn])

            pi_my_authorities = pi_authorities

            # Summary all
            # @qursaan
            # iterate on the requests and check if the authority matches a prefix startswith an authority on which the user is PI
            requests = get_requests()

            # requests = get_requests(queried_pending_authorities)
            for request in requests:
                auth_hrn = request['authority_hrn']
                if user.is_admin == 1 and auth_hrn:
                    for my_auth in pi_my_authorities:
                        if auth_hrn.startswith(my_auth):
                            # dest = ctx_my_authorities
                            request['allowed'] = 'allowed'

                if 'allowed' not in request:
                    request['allowed'] = 'denied'
                # print "authority for this request", auth_hrn

                if auth_hrn in pi_my_authorities:
                    # dest = ctx_my_authorities
                    if not auth_hrn in ctx_my_authorities:
                        ctx_my_authorities[auth_hrn] = []
                    ctx_my_authorities[auth_hrn].append(request)

        context = super(ValidatePendingView, self).get_context_data(**kwargs)
        context['my_authorities'] = ctx_my_authorities
        # context['sub_authorities']   = ctx_sub_authorities
        # context['delegation_authorities'] = ctx_delegation_authorities
        context['is_admin'] = user.is_admin
        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Validate Requests'
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('Validation', page.request)
        # so we can sho who is logged
        context['username'] = usera.username

        # XXX We need to prepare the page for queries
        context.update(page.prelude_env())

        return context
