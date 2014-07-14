from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
#from Library.profile.models import Profile_addition
from django.views.generic.edit import UpdateView
#from Library.book_library.views import LoginRequiredView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import forms



class ProfileFormView(UpdateView):
    model = User
    form_class = forms.ProfileForm

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == int(kwargs['pk']):
            return super(ProfileFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")


class UsersView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return super(UsersView, self).get(request, *args, **kwargs)