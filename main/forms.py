from django import forms
from .models import Media
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))  

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if 3 <= len(username) <= 25:
            return username
        raise forms.ValidationError('Username must be between 3 and 25 characters long.')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
        
    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        elif len(cd['password1']) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return cd['password2']
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
