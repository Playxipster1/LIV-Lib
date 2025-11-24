from django import forms
from .models import Order

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