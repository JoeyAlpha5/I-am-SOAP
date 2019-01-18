from django import forms

class shippingForm(forms.Form):
    street = forms.CharField(max_length=150, required=True)
    apartment = forms.CharField(max_length=150, required=False)
    city = forms.CharField(max_length=150, required=True)
    Province = forms.CharField(max_length=150, required=True)
    Country = forms.CharField(max_length=150, required=True)

class accountForm(forms.Form):
    name = forms.CharField(max_length=150, required=True)
    surname = forms.CharField(max_length=150, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={"type":"password"}), required=False)
    newPass = forms.CharField(widget=forms.TextInput(attrs={"type":"password"}), required=False)
    confPass = forms.CharField(widget=forms.TextInput(attrs={"type":"password"}), required=False)