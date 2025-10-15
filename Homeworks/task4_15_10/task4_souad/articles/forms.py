from django import forms
from .models import Article


class ArticleForm(forms.Form):
    title = forms.CharField(
        label='article_title',
        max_length=200,
        widget=forms.TextInput()
    )
    content = forms.CharField(
        label='article_content',
        widget=forms.Textarea()
    )

    def clean_title(self):
        cleaned_data = super().clean()
        name= self.cleaned_data['title'].strip()
        if not name.isalpha():
            raise forms.ValidationError('Title must be a word')
        return name

    def clean_content(self):
        cleaned_data = super().clean()
        content = self.cleaned_data['content'].strip()
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 30 characters long')
        return content