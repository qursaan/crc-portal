from django.shortcuts import render

from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items
from unfold.loginrequired import FreeAccessView


# ************ Support Page ***************
# splitting the 2 functions done here
# GET is for displaying the empty form
# POST is to process it once filled - or show the form again if anything is missing
class SupportView(FreeAccessView):
    # template_name = "support-view.html"

    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'support-view.html', {
            'topmenu_items': topmenu_items('support', request),
            'username': UserAccessProfile(request).username,
            'title': 'Support',
        })


class GuideView(FreeAccessView):
    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'guide-view.html', {
            'topmenu_items': topmenu_items('Guide', request),
            'username': UserAccessProfile(request).username,
            'title': 'Portal Guide',
        })


class TGuideView(FreeAccessView):
    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'tguide-view.html', {
            'topmenu_items': topmenu_items('Guide', request),
            'username': UserAccessProfile(request).username,
            'title': 'Portal Teaching Guide',
        })
