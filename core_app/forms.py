from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ad, Review


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'city', 'title', 'description', 'price', 'contact_phone', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'contact_phone': 'Телефон (показывается по кнопке «Показать номер»)',
            'image_url': 'URL фотографии (необязательно)',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} / 5') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите отзыв об авторе объявления...'}),
        }
        labels = {
            'rating': 'Оценка',
            'comment': 'Комментарий',
        }
