from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, Tea
from django.shortcuts import render

def home(request):
    context = {
        'active_page': 'home',
    }
    return render(request, 'tea/home.html', context)

def index(request):
    context = {
        'active_page': 'index',
    }
    return render(request, 'tea/main.html', context)

def homepage(request):
    context = {
        'active_page': 'homepage',
    }
    return render(request, 'homepage.html', context)

def contact(request):
    context = {
        'active_page': 'contact',
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'active_page': 'about',
    }
    return render(request, 'about.html', context)

    
def subs(request):
    context = {
        'active_page': 'subs',
    }
    return render(request, 'tea/subs.html', context)

def tea_detail(request, id, slug):
    tea = get_object_or_404(Tea, id=id, slug=slug, available=True)
    return render(request, 'tea/detail.html', {'tea': tea})

def auth(request):
    
    return render(request, 'user/auth.html')

