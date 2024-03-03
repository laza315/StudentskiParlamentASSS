from django import forms
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Anketa, BackUpKod, Pitanja, Izbori
from django.utils import timezone

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
    smer = forms.ChoiceField(choices=Anketa.SMER_CHOICES)
    tip_ankete = forms.ChoiceField(choices=Anketa.AnketaType.choices, label='Tip ankete') 

    def clean_vreme_do(self):
        vreme_do = self.cleaned_data.get('vreme_do')
        if vreme_do <= timezone.now() + timezone.timedelta(minutes=15):
            raise forms.ValidationError("Aktivnost mora biti duza od 10h")
        return vreme_do
    
    class Meta:
        model = Anketa
        fields = ['naziv', 'smer', 'tip_ankete', 'godina', 'broj_kodova', 'broj_pitanja', 'vreme_do', 'opis_ankete']
        labels = {
            'naziv': 'Naziv',
            'godina': 'Godina',
            'opis_ankete': 'Opis Ankete',
            'broj_kodova': 'Broj studenata',
            'broj_pitanja': 'Broj Pitanja'
        }
        widgets = {
            'naziv': forms.TextInput(attrs={'class': 'form-control'}),
            'godina': forms.NumberInput(attrs={'class': 'form-control', 'max': 3, 'min': 1}),
            'opis_ankete': forms.Textarea(attrs={'class': 'form-control'}),
            'broj_kodova': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'broj_pitanja': forms.NumberInput(attrs={'class': 'form-control', 'max': 5, 'min': 1}),
            'vreme_do': DateTimeInput(attrs={'type': 'datetime-local'})
        }
        
class BackupCodesForm(ModelForm):
    class Meta:
        model = BackUpKod
        fields = ['code_value', 'anketa']


class PitanjaForm(ModelForm):
    class Meta:
        model = Pitanja
        fields = ['question_text']
        labels = {
            'question_text': 'Text Pitanja',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VotesForm(ModelForm):
    votes = forms.ChoiceField(choices=Izbori.VOTE_CHOICES, label='Glasovi', initial='3') 
    class Meta:
        model = Izbori
        fields = ['votes']
        

# class IzboriForm(ModelForm):
#     izbori = forms.ChoiceField(choices=Izbori.VOTE_CHOICES)
#     class Meta:
#         model = Izbori
#         fields = ['votes']
#         labels = {
#             'votes': 'Votes',
#            }
          
    
        
