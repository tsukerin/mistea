from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, Tea
from django.shortcuts import render

def index(request):
    return render(request, 'tea/index.html')
# def home(request):
#     return render(request, 'tea/home.html')
    
def tea_list(request, category_slug=None):
    category = None
    categories = TeaCategory.objects.all()
    teas = Tea.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(TeaCategory, slug=category_slug)
        teas = teas.filter(category=category)
    return render(request, 'tea/list.html', {'category': category, 'categories': categories, 'teas': teas})

def tea_detail(request, id, slug):
    tea = get_object_or_404(Tea, id=id, slug=slug, available=True)
    return render(request, 'tea/detail.html', {'tea': tea})


