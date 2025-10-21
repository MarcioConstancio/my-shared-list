# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    # O campo de email já será tratado como o principal pelo UserCreationForm
    # por causa das nossas mudanças no modelo.
    telefone = forms.CharField(max_length=15, required=True, help_text='Ex: (11) 98765-4321')

    class Meta(UserCreationForm.Meta):
        model = User
        # O campo 'email' já é o principal. O campo 'username' não é mais necessário aqui.
        fields = ('email', 'telefone')