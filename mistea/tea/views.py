import uuid
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from mistea.settings import ID_SHOP, SECRET_KEY
from .models import Subscription, TeaCategory, Tea
from user.models import UserProfile, UserSubscription, User
from django.shortcuts import render
from .forms import DeleteSubscriptionForm, LoginForm, ProfileForm, RegForm, UserSubscriptionForm
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.contrib import messages
from yookassa import Configuration, Payment

def homepage(request):
    context = {
        'active_page': 'homepage',
    }
    return render(request, 'homepage.html', context)

def contact(request):
    context = {
        'active_page': 'contact',
    }
    return render(request, 'tea/contact.html', context)

def about(request):
    context = {
        'active_page': 'about',
    }
    return render(request, 'tea/about.html', context)

def subscription_detail(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    return render(request, 'tea/detail.html', {'subscription': subscription})


class OrderSub(LoginRequiredMixin, View):
    login_url = "login"
    form_class = UserSubscriptionForm
    template_name = 'tea/order.html'
    redirect_field_name = 'next'
    form_model = UserSubscription
    success_url = reverse_lazy("payment")
    Configuration.configure(ID_SHOP, SECRET_KEY)
    def get(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            form = self.form_class(initial={'sub_id': subscription})
        except:
            form = self.form_class()
        return render(request, self.template_name, {'order': subscription, 'form': form})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Чтобы приобрести подписку, пожалуйста, войдите в аккаунт.')
            return super().dispatch(request, *args, **kwargs)
    
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
        if user_profile.subscription == 1:
            return redirect('checkout:already')
    
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, subscription_id):
        form = self.form_class(request.POST)

        if form.is_valid():
            subscription = get_object_or_404(Subscription, pk=subscription_id)
            personalized_identifier = str(uuid.uuid4())
            form.instance.personalized_identifier = personalized_identifier
            form.instance.sub_id = subscription
            form.save()
            payment = Payment.create({
                "amount": {
                    "value": subscription.price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri(reverse('checkout:success', kwargs={'personalized_identifier': personalized_identifier})),
                },
                "capture": True,
                "description": f'Подписка: {subscription.name}.'
            }, uuid.uuid4())
            confirmation_url = payment.confirmation.confirmation_url
            return redirect(confirmation_url, personalized_identifier=personalized_identifier)
        else:
            print(form.errors)

        subscription = get_object_or_404(Subscription, pk=subscription_id)
        return render(request, self.template_name, {'order': subscription, 'form': form})
#----------------------------------------------------------------------------------------------------------------------------
#Аутентификация и профиль

class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    form_class = ProfileForm
    template_name = 'registration/lk.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form, 'user_profile': user_profile})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста, войдите в аккаунт, чтобы просмотреть профиль.')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form = self.form_class(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
        else:
            return render(request, self.template_name, {'form': form, 'user_profile': user_profile})
    

class RegisterView(CreateView):
    form_class = RegForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = UserProfile.objects.create(user=self.object)
        return response
    
class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class DeleteSubscriptionView(View):
    template_name = 'registration/lk.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = DeleteSubscriptionForm(request.POST)

        if form.is_valid():
            user_profile = request.user.userprofile
            user_profile.subscription = 0
            user_profile.days_remaining = 0
            user_profile.save()

            return redirect('profile')

        return render(request, self.template_name, {'form': form})