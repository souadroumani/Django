from django.shortcuts import render
from .models import Post
from .forms import ContactForm

# Create your views here.

def home_view(request):
    return render(request, 'blog/home.html')

def posts_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/posts.html', {'posts': posts})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return render(request, 'blog/thanks.html', {'name': name})

    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'blog/contact.html', {'form': form})

