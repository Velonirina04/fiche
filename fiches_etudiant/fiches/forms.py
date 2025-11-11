from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Fiche

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FicheForm(forms.ModelForm):
    class Meta:
        model = Fiche
        fields = ['nom', 'prenom', 'photo', 'filiere','niveau', 'interets', 'description', 'avis_responsable']
        widgets = {
            'interets': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'avis_responsable': forms.Textarea(attrs={'rows': 3}),
        }