from django import forms

class login_form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    widgets = {
        'password': forms.PasswordInput(),
    }

class employee_login_form(forms.Form):
    e_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    widgets = {
        'password': forms.PasswordInput(),
    }

class register(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    gender = forms.CharField(max_length=20)
    address = forms.CharField(max_length=60)
    phone_number = forms.CharField(max_length=10)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    widgets = {
        'password': forms.PasswordInput(),
    }