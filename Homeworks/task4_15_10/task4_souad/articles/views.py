from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from .forms import ArticleForm
from .models import Article
from django.urls import reverse_lazy

def article_list(request):
    qs = Article.objects.all().order_by('-created_at')
    return render(request, 'articles/article_list.html', {'articles': qs})

class ArticleCreateView(FormView):
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url= reverse_lazy('list')

    def form_valid(self, form):
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        Article.objects.create(title=title, content=content)
        return  super().form_valid(form)

    def form_invalid(self, form):
        print("Something went wrong, please try again")
        print(form.errors)
        return super().form_invalid(form)

