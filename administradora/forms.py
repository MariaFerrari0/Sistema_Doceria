from django import forms


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