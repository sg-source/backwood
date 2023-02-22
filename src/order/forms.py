from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    SHIPPING = (
        (False, 'Free (during 1 month)'),
        (True, '$15 (at most next day)'),
    )
    
    firstname = forms.CharField(label='firstname', required=True,
                                widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                              'autofocus': 'None'}))
    lastname = forms.CharField(label='lastname', required=True,
                               widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                             'autofocus': 'None'}))
    email = forms.EmailField(label='email', required=True,
                             widget=forms.EmailInput(attrs={'autocomplete': 'on',
                                                            'autofocus': 'None'}))
    address = forms.CharField(label='address', required=True,
                              widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                            'autofocus': 'None'}))
    city = forms.CharField(label='city', required=True,
                           widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                         'autofocus': 'None'}))
    postal_code = forms.IntegerField(label='postal code',
                                     error_messages={'invalid': 'Enter a valid postal code'},
                                     required=True,
                                     widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                                   'autofocus': 'None'}))
    notes = forms.CharField(label='notes', max_length=250,
                            required=False, widget=forms.Textarea(attrs={'autocomplete': 'on',
                                                                         'autofocus': 'None'}))
    phone = forms.IntegerField(label='phone', required=True,
                               error_messages={'invalid': 'Enter a valid phone'},
                               widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                             'autofocus': 'None'}))
    
    shipping = forms.BooleanField(required=False, label='shipping',
                                  widget=forms.RadioSelect(choices=SHIPPING))
    
    class Meta:
        model = Order
        fields = ('firstname', 'lastname', 'email', 'phone', 'address',
                  'postal_code', 'city', 'notes', 'shipping')


class PaymentForm(forms.Form):
    name = forms.CharField(label='name', max_length=20, required=True,
                           widget=forms.TextInput(attrs={'id': 'name',
                                                         'autocomplete': 'off',
                                                         'autofocus': 'None'}))
    cardnumber = forms.CharField(label='card number', required=True,
                                 widget=forms.TextInput(attrs={
                                     'id': 'cardnumber',
                                     'autocomplete': 'off',
                                     'pattern': r'[0-9]{4}\s([0-9]{4}\s[0-9]{4}|[0-9]{6})\s[0-9]{4}',
                                     'inputmode': 'numeric',
                                     'autofocus': 'None',
                                     'disabled': 'on'})
                                 )
    expiration = forms.CharField(label='expiration', required=True,
                                 widget=forms.TextInput(attrs={'id': 'expirationdate',
                                                               'autocomplete': 'off',
                                                               'pattern': '[0-9]*\/[0-9]*',
                                                               'inputmode': 'numeric',
                                                               'autofocus': 'None'}))
    securitycode = forms.CharField(label='security code', required=True,
                                   widget=forms.TextInput(attrs={'id': 'securitycode',
                                                                 'autocomplete': 'off',
                                                                 'pattern': '[0-9]*',
                                                                 'inputmode': 'numeric',
                                                                 'autofocus': 'None',
                                                                 'disabled': 'on'}))
    
    class Meta:
        fields = ('name', 'cardnumber', 'expiration', 'securitycode')