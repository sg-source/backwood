from django import forms


class ContactForm(forms.Form):
    firstname = forms.CharField(label='firstname',
                                required=True,
                                widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                              'placeholder': 'Name', }))
    email = forms.EmailField(label='email',
                             required=True,
                             widget=forms.EmailInput(attrs={'autocomplete': 'on',
                                                            'placeholder': 'Email', }))
    phone = forms.IntegerField(label='phone',
                               required=True,
                               error_messages={'invalid': 'Enter a valid phone'},
                               widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                             'placeholder': 'Phone', }))
    subject = forms.CharField(label='subject',
                              required=True,
                              max_length=40,
                              widget=forms.TextInput(attrs={'autocomplete': 'on',
                                                            'placeholder': 'Subject', }))
    
    message = forms.CharField(label='message',
                              max_length=250,
                              required=True, widget=forms.Textarea(attrs={'autocomplete': 'on',
                                                                          'placeholder': 'Your message', }))
    
    class Meta:
        fields = (
            'firstname',
            'email',
            'phone',
            'subject',
            'message',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.pop("autofocus", None)
        self.fields['email'].widget.attrs.pop("autofocus", None)
        self.fields['phone'].widget.attrs.pop("autofocus", None)
        self.fields['message'].widget.attrs.pop("autofocus", None)
