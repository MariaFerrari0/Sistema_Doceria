
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CadastroClienteForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome',
            'class': 'input-control'
        })
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu sobrenome',
            'class': 'input-control'
        })
    )

    email = forms.EmailField(
        label='E-mail',
        max_length=150,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'input-control'
        })
    )

    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '(00) 00000-0000',
            'class': 'input-control'
        })
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'class': 'input-control',
            'autocomplete': 'new-password'
        })
    )

    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'class': 'input-control',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')

        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        email = self.cleaned_data['email']

        usuario.username = email
        usuario.email = email

        if commit:
            usuario.save()

        return usuario
