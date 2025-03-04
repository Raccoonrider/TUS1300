from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from users.forms import *

@method_decorator(login_required, name="dispatch")
class UserProfileCreateUpdate(FormView):
    template_name = "users/user_profile.html"
    form_class = UserProfileForm

    def get_form(self, form_class=UserProfileForm) -> UserProfileForm:
        instance = self.request.user.profile
        if instance is not None:
            return form_class(instance=instance, **self.get_form_kwargs())
        return super().get_form(form_class)

    def form_valid(self, form) -> HttpResponse:
        self.request.user.profile = form.instance
        form.save()
        self.request.user.save()
        return user_redirect(self.request)    

def user_redirect(request):
    redirect_url = request.session.get('redirect', '/')
    return HttpResponseRedirect(redirect_url)
