from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Book, User
from django.contrib.auth import get_user_model

User = get_user_model()

# Main book form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'category', 'condition', 'status', 'price', 'quantity', 'image']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        # Optional: Add placeholders or widgets for styling
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter book title'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Describe your book'})
        self.fields['price'].widget.attrs.update({'min': 0})
        self.fields['quantity'].widget.attrs.update({'min': 1})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")