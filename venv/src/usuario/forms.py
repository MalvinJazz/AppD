# -*- coding: utf-8 -*-

from django import forms

from .models import Usuario

class InicioForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserCreationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellidos',
            'username',
            'correo',
            'tipo',
            'institucion',
            'zona'
        ]

    def clean_password1(self):

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if password and password1 and len(password) < 8:
            raise forms.ValidationError("Ingrese una contraseña más larga.")

        return password1

    def save(self, commit=False):

        usuario = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()

        return user
