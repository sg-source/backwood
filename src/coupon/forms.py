from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label='code',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Coupon Code',
            'id': 'coupon_code',
            'class': 'input-text',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'autofocus': False})
