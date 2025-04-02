from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import re

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email',
            'autofocus': True
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Contraseña'
        }),
    )

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email',
            'autofocus': True,
            'autocomplete': 'off'
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Contraseña',
            'autocomplete': 'new-password'
        }),
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Repetir contraseña',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        model = User
        fields = ["email"]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password  = cleaned_data.get("password")
        repeat_password  = cleaned_data.get("repeat_password")
        if password:
            if len(password) < 10:
                raise forms.ValidationError("La contraseña debe tener al menos 10 caracteres.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("La contraseña debe tener al menos una mayúscula.")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("La contraseña debe tener al menos una minúscula.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("La contraseña debe tener al menos un número.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError("La contraseña debe tener al menos un caracter especial.")
        if password  and repeat_password  and password  != repeat_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class CustomPasswordResetForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'
        }),
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Repetir nueva contraseña',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        model = User
        fields = ["id"]

    def clean(self):
        cleaned_data = super().clean()
        password  = cleaned_data.get("password")
        repeat_password  = cleaned_data.get("repeat_password")
        
        if password:
            if len(password) < 10:
                raise forms.ValidationError("La contraseña debe tener al menos 10 caracteres.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("La contraseña debe tener al menos una mayúscula.")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("La contraseña debe tener al menos una minúscula.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("La contraseña debe tener al menos un número.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError("La contraseña debe tener al menos un caracter especial.")
        if password  and repeat_password  and password  != repeat_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, user, commit=True):
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user