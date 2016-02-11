from django.shortcuts import render

from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import FreeAccessView


# splitting the 2 functions done here
# GET is for displaying the empty form
# POST is to process it once filled - or show the form again if anything is missing
class ExperimentView(FreeAccessView):
    template_name = "experiment-view.html"

    def get(self, request):
        return self._display(request)

    def _display(self, request):
        return render(request, 'experiment-view.html', {
            'topmenu_items': topmenu_items('experiment', request),
            'username': the_user(request),
            'title': 'Experiment Tools Information',
        })
