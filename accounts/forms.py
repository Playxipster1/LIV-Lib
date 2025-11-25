from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Ваш email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Вае имя',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Вау фамилию',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Придумайте имя пользователя'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Имя пользователя должно состоять хотябы из трех символов")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TelInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия', 
            'email': 'Email адрес'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})