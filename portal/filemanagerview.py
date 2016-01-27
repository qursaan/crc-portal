__author__ = 'pirate'
from django.shortcuts           import render
from unfold.loginrequired       import FreeAccessView
from ui.topmenu                 import topmenu_items, the_user


class FileManagerView (FreeAccessView):
    template_name = "filemanager-view.html"

    def get (self, request):
        return self._display (request)

    def _display (self, request):
        return render(request, 'filemanager-view.html', {
                'topmenu_items': topmenu_items('filemanager', request),
                'username': the_user(request),
                'title': 'User Cloud Disk Manager',
                })



