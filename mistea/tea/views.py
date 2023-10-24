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
    return render(request, 'tea/index.html', context)

def index2(request):
    context = {
        'active_page': 'index',
    }
    return render(request, 'tea/index2.html', context)

def tea_list(request):
    category = None
    categories = TeaCategory.objects.all()
    teas = Tea.objects.filter(available=True)
    # if category_slug:
    #     category = get_object_or_404(TeaCategory, slug=category_slug)
    #     teas = teas.filter(category=category)
    return render(request, 'tea/tea_list.html', {'category': category, 'categories': categories, 'teas': teas})

    
def subs(request):
    context = {
        'active_page': 'subs',
    }
    return render(request, 'tea/subs.html', context)

def tea_detail(request, id, slug):
    tea = get_object_or_404(Tea, id=id, slug=slug, available=True)
    return render(request, 'tea/detail.html', {'tea': tea})


