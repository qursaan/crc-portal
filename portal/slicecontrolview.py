__author__ = 'pirate'
import json
from random import randint
from django.template.loader     import render_to_string
from unfold.loginrequired    import LoginRequiredAutoLogoutView
from unfold.page             import Page
from ui.topmenu              import topmenu_items, the_user
#
from portal.models      import Reservation, ReservationDetail, TestbedImage, UserImage, VirtualNode
from portal.navigation  import load_image, save_image, omf_exe, remote_node
from portal.actions     import get_user_by_email
#
from django.http                        import HttpResponse, HttpResponseRedirect
from django.contrib                     import messages
from django.contrib.auth.decorators     import login_required
from django.template.loader             import render_to_string


class SliceControlView(LoginRequiredAutoLogoutView):
    template_name = "slice-control-view.html"

    def dispatch(self, *args, **kwargs):
        return super(SliceControlView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        page = Page(self.request)
        page.add_js_files(["js/jquery.validate.js", "js/my_account.register.js", "js/my_account.edit_profile.js" ] )
        page.add_css_files(["css/onelab.css", "css/plugin.css"])

        image_list = TestbedImage.objects.all()
        user = get_user_by_email(the_user(self.request))
        user_image_list = []
        if user:
            user_image_list = UserImage.objects.filter(user_ref=user).all()
        node_list = []
        slice_id = page.request.session.get('slice_id', '')
        if slice_id is not None:
            current_slice = Reservation.objects.get(id=slice_id)
            node_list = ReservationDetail.objects.filter(reservation_ref=current_slice)

        if not slice_id:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/portal/lab/current/")

        #active_page = page.request.session.get('active_page','0')

        output_script =''
        #try:
        #    if active_page==3:
        #        output_script = page.request.session.get('output','')
        #finally:
        #    pass

        context = super(SliceControlView, self).get_context_data(**kwargs)
        context['image_list'] = image_list
        context['user_image_list'] = user_image_list
        context['node_list'] = node_list
        # context['active_page'] = active_page
        context['output'] = output_script
        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Control Testbed Panel'
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('Control Panel', page.request)  # @qursaan change from _live
        # so we can sho who is logged
        context['username'] = the_user(self.request)
        #context ['firstname'] = config['firstname']
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def control_remote_node(request):
    return remote_node(request)


@login_required
def control_load_image(request):
    return load_image(request)


@login_required
def control_save_image(request):
    return save_image(request)


@login_required
def control_exe_script(request):
    return omf_exe(request)


@login_required
def create_exe_post(request):
    if request.method == 'POST':
        script_text = request.POST.get('the_post')
        response_data = {}
        #savefile
        file_name = str(randint(1, 1000000)) +".rb"
        text_file = open(file_name, "w")
        text_file.write("%s" % script_text)
        text_file.close()
        t = omf_execute(file_name)
        request.session['active_page'] = 3
        response_data['result'] = t

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def control_load_sample(request):
    if request.method == 'POST':
        type = request.POST.get('the_post')
        response_data = {}

        t = "10"
        if type=="sample-1":
            t = render_to_string('sample-ping.rb')
        elif type=="sample-2":
            t = render_to_string('sample-urc.rb')

        response_data['result'] = t

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

