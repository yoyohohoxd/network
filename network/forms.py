from django.forms import ModelForm
from django import forms
from .models import NewPost

class NewPostForm(ModelForm):
    class Meta:
        model = NewPost
        fields = ["post_text"]