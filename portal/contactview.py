from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string

from crc.settings import SUPPORT_EMAIL
from portal.forms import ContactForm
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import FreeAccessView


# from django.views.generic      import View
# splitting the 2 functions done here
# GET is for displaying the empty form
# POST is to process it once filled - or show the form again if anything is missing


class ContactView(FreeAccessView):
    def post(self, request):
        form = ContactForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            authority = form.cleaned_data['authority']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']  # email of the sender
            cc_myself = form.cleaned_data['cc_myself']

            # recipients = authority_get_pi_emails(authority_hrn)
            recipients = [SUPPORT_EMAIL]
            if cc_myself:
                recipients.append(email)

            msg = render_to_string('contact-support-email.txt', form.cleaned_data)
            send_mail("CRC lab user %s submitted a query " % email, msg, email, recipients)
            return render(request, 'contact_sent.html')  # Redirect after POST
        else:
            return self._display(request, form)

    def get(self, request):
        return self._display(request, ContactForm())  # A fresh unbound form

    def _display(self, request, form):
        return render(request, 'contact-view.html', {
            'form': form,
            'topmenu_items': topmenu_items('Contact', request),
            'username': the_user(request),
            'title': 'Contact Us',
        })
