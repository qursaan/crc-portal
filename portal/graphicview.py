__author__ = 'pirate'

from django.shortcuts     import render
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu           import topmenu_items, the_user
from unfold.page          import Page


class GraphicBuilderView (LoginRequiredAutoLogoutView):
    template_name = "gbuilder-view.html"

    def dispatch(self, *args, **kwargs):
        return super(GraphicBuilderView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        prelude_env = page.prelude_env()
        context = super(GraphicBuilderView, self).get_context_data(**kwargs)
        context['title'] = 'Graphic Builder Tools'
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('Graphic Builder', page.request)  # @qursaan change from _live
        # so we can sho who is logged
        context['username'] = the_user(self.request)
        context.update(prelude_env)
        return context
