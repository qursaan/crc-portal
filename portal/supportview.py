from django.shortcuts import render
from unfold.loginrequired import FreeAccessView
from ui.topmenu import topmenu_items, the_user


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
            'username': the_user(request),
            'title': 'Support',
        })


class GuideView(FreeAccessView):
    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'guide-view.html', {
            'topmenu_items': topmenu_items('Guide', request),
            'username': the_user(request),
            'title': 'Portal Guide',
        })


class TGuideView(FreeAccessView):
    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'tguide-view.html', {
            'topmenu_items': topmenu_items('Guide', request),
            'username': the_user(request),
            'title': 'Portal Teaching Guide',
        })
