from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Anketa

# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class AnketaForm(ModelForm):
    class Meta:
        model = Anketa
        fields = ['naziv','opis_ankete', 'broj_kodova']
        labels = {
            'naziv': 'Naziv',
            'opis_ankete': 'Opis Ankete',
            'broj_kodova': 'Broj studenata'        
        }
        widgets = {
            'naziv': forms.TextInput(attrs={'class': 'form-control'}),
            'opis_ankete': forms.TextInput(attrs={'class': 'form-control'}),
            'broj_kodova': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }
        

