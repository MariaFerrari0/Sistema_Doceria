from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário / E-mail',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário', 'class': 'input-control'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class': 'input-control'})
    )
    lembrar_me = forms.BooleanField(
        label='Lembrar-me',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-control'})
    )


class PerfilAdministradoraForm(forms.ModelForm):
    nova_senha = forms.CharField(
        label='Nova Senha (deixe em branco para não alterar)',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'input-control', 'placeholder': 'Digite uma nova senha se quiser alterar'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de Usuário',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-control'}),
            'last_name': forms.TextInput(attrs={'class': 'input-control'}),
            'username': forms.TextInput(attrs={'class': 'input-control'}),
            'email': forms.EmailInput(attrs={'class': 'input-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        nova_senha = self.cleaned_data.get('nova_senha')
        # Criptografa a nova senha com PBKDF2/SHA-256 se for informada
        if nova_senha:
            user.set_password(nova_senha)
        if commit:
            user.save()
        return user