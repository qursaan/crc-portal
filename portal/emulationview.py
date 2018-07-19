__author__ = 'pirate'

from unfold.loginrequired   import LoginRequiredAutoLogoutView


# ********** View Testbed Map Page *********** #
class EmulationView(LoginRequiredAutoLogoutView):
    template_name = "node-emulation-view.html"

    def dispatch(self, *args, **kwargs):
        return super(EmulationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmulationView, self).get_context_data(**kwargs)
        return context