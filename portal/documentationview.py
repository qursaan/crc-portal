from django.shortcuts import render

from ui.topmenu import topmenu_items
from unfold.loginrequired import FreeAccessView


# splitting the 2 functions done here
# GET is for displaying the empty form
# POST is to process it once filled - or show the form again if anything is missing
class DocumentationView(FreeAccessView):
    template_name = "documentation-view.html"

    def _display(self, request):
        return render(request, 'documentation-view.html', {
            'topmenu_items': topmenu_items('FAQ', request),
        })
