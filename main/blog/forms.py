from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):

    from_email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Email',
            'tabindex': '1'
        }), required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'style': 'max-width: 300px; max-height: 300px; height: 150px;',
            'placeholder': 'Message',
            'tabindex': '2'
        }), required=True)
    subject = forms.CharField(widget=forms.HiddenInput(), required=False)
