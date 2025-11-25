from django import forms
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number', 'email', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите полный адрес доставки'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Дополнительные пожелания к заказу (необязательно)'
            }),
        }
        labels = {
            'shipping_address': 'Адрес доставки',
            'phone_number': 'Номер телефона',
            'email': 'Email',
            'notes': 'Примечания к заказу',
        }

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