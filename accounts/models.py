from django.db import models
from contatos.models import Contato
from django import forms

class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ("user", "id_by_user",)
