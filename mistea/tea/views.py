from django.shortcuts import redirect, render, get_object_or_404
from .models import TeaCategory, Tea
from django.shortcuts import render
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

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

def subscribe(request):
    return render(request, 'subscribe.html')

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

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "user/auth.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "user/registration.html", {"form": form, "msg": msg, "success": success})


def user_logout(request):
    logout(request)
    msg = 'Form is not valid'
    form = LoginForm(request.POST or None)
    return render(request, '', {"form": form, "msg": msg})

