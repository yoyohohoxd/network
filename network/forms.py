from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django import forms
from .models import NewPost

class NewPostForm(ModelForm):
    class Meta:
        model = NewPost
        fields = ["post_text"]

        widgets = {
            "post_text": forms.Textarea(attrs={'placeholder': 'Anything you feel like sharing today?'})
        }

        def __init__(self, *args, **kwargs):
            super(NewPostForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = False