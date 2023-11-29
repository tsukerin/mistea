from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .models import Subscription, TeaCategory, Tea, UserSubscription
from django.shortcuts import render
from .forms import LoginForm, ProfileForm, RegForm, UserSubscriptionForm
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.contrib import messages



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

class OrderSub(LoginRequiredMixin, View):
    login_url = "login"
    form_class = UserSubscriptionForm
    template_name = 'subscr.html'
    redirect_field_name = 'next'
    form_model = UserSubscription
    success_url = reverse_lazy("homepage")
    def get(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            form = self.form_class(initial={'sub_id': subscription})
        except:
            form = self.form_class()

        return render(request, self.template_name, {'subscr': subscription, 'form': form})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:   
            messages.warning(request, 'Чтобы преобрести подписку, УМОЛЯЮ, войдите в аккаунт.')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, subscription_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.sub_id = Subscription.objects.get(id=subscription_id)
            form.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
        
        subscription = Subscription.objects.get(id=subscription_id)
        return render(request, self.template_name, {'subscr': subscription, 'form': form})

#-----------------------------------------------------------------------------------------------------------------------------
#Аутентификация

class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста, войдите в аккаунт, чтобы просмотреть профиль.')
        return super().dispatch(request, *args, **kwargs)
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


