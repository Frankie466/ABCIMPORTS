# store/forms.py
from django import forms

class OrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    county = forms.CharField(max_length=100, required=True)
    town = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=10, required=True)
    alt_phone = forms.CharField(max_length=10, required=False)
   