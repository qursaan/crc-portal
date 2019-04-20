from django.shortcuts import render

from ui.topmenu import topmenu_items
from unfold.loginrequired import FreeAccessView


class DocumentationView(FreeAccessView):
    template_name = "documentation-view.html"

    def _display(self, request):
        return render(request, 'documentation-view.html', {
            'topmenu_items': topmenu_items('FAQ', request),
        })
