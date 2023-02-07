from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm


class LoginUser(LoginView):
    success_message = 'The user with e-mail %(email) has been successfully created.'
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True
    authentication_form = UserLoginForm
    success_url = reverse_lazy('main:index')
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        super().form_valid(form)
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)
        return HttpResponseRedirect(self.get_success_url())


class LogoutUser(LogoutView):
    next_page = reverse_lazy('main:index')


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    
    def get_success_message(self, cleaned_data):
        return mark_safe(u'The user with e-mail <strong>{email}</strong> has been successfully created.'.format(
            email=cleaned_data.get('email')))


class UserDetails(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    model = get_user_model()
    context_object_name = 'user'
    template_name = 'authapp/profile.html'
    
    def get_object(self, queryset=None):
        """Overriding method for accessing only current authenticated user"""
        
        if queryset is None:
            queryset = self.get_queryset()
        
        pk = self.kwargs.get(self.pk_url_kwarg)
        
        if pk is not None:
            queryset = queryset.filter(Q(pk=pk) & Q(pk=self.request.user.pk))

        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        orders = user.orders.all()

        context['orders'] = orders
        return context
        
