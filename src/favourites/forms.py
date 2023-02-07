from django import forms


class FavouritesAddProductForm(forms.Form):
    product_id = forms.IntegerField(required=True)
