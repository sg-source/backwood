from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    firstname = forms.CharField(
        label='firstname', required=True,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'autocomplete': 'off'})
    )
    email = forms.EmailField(
        label='email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'autocomplete': 'on',
                                      'autofocus': 'None',
                                      'pattern': r'^[a-zA-Z0-9.!#$%&'
                                                 r'’*+/=?^_`{|}~-]+@'
                                                 r'[a-zA-Z0-9-]+(?:\
                                                 .[a-zA-Z0-9-]{2,})',
                                      'placeholder': 'www@web.com'})
    )
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    approval = forms.BooleanField(
        label='I agree to the Terms & Conditions',
        required=True, initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox-input'})
    )
    
    class Meta:
        model = User
        fields = ['firstname', 'email', 'password1', 'password2', 'approval']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop("autofocus", None)


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label='email',
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'autocomplete': 'on'})
    )
    
    password = forms.PasswordInput()
    remember_me = forms.BooleanField(
        label='Keep me signed in',
        required=False, initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox-input'})
    )
    
    class Meta:
        model: User
        fields = ['email', 'password']
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields.pop('username')
    
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    firstname = forms.CharField(
        label='firstname',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                     'autocomplete': 'off'})
    )
    lastname = forms.CharField(
        label='lastname',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'autocomplete': 'off'})
    )
    email = forms.EmailField(
        label='email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'autocomplete': 'on',
                                      'autofocus': 'None'}))
    phone = forms.IntegerField(
        label='phone',
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'on',
                                      'autofocus': 'None'})
    )
    
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'phone')
