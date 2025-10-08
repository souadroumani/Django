from django import forms



class ContactForm(forms.Form):
    name = forms.CharField(label='your name ',max_length=100)
    email = forms.EmailField(label='your email ',max_length=100)
    message = forms.CharField(widget=forms.Textarea,label='your message')

