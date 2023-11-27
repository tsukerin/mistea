from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .models import Subscription, TeaCategory, Tea
from django.shortcuts import render
from .forms import LoginForm, ProfileForm, RegForm
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View


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

def subscription_detail(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    return render(request, 'detail.html', {'subscription': subscription})


#-----------------------------------------------------------------------------------------------------------------------------
#Аутентификация
def login_view(request):
    # form = LoginForm(request.POST or None)

    # msg = None

    # if request.method == "POST":

    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect("/")
    #         else:
    #             msg = 'Invalid credentials'
    #     else:
    #         msg = 'Error validating the form'

    return render(request, "registration/login.html")

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = RegForm()

    return render(request, "user/registration.html", {"form": form, "msg": msg, "success": success})


# def user_logout(request):
#     logout(request)
#     msg = 'Form is not valid'
#     form = LoginForm(request.POST or None)
#     return render(request, '', {"form": form, "msg": msg})

# def index(request):
#     context = {'segment': 'index'}

#     # html_template = loader.get_template('home/index.html')
#     # return HttpResponse(html_template.render(context, request))

class ProfileView(LoginRequiredMixin, View):
    login_url = "/login/"
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    redirect_field_name = "registration/profile.html"
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
    

class RegisterView(CreateView):
    form_class = RegForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


