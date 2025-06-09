from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="Ism Familiya", max_length=100)
    phone = forms.CharField(label="Telefon", max_length=12)
    address = forms.CharField(label="Manzil", widget=forms.Textarea)