from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['author', 'header', 'text', 'rating_art_nws', 'categories']

       def clean(self):
           cleaned_data = super().clean()
           header = cleaned_data.get("header")
           text = cleaned_data.get("text")

           if header == text:
               raise ValidationError(
                   "Заголовок не должен быть таким как содержание."
               )

           return cleaned_data


