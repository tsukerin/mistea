from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from tea.models import Subscription
from django.contrib.auth.models import User


# Create your models here.

class UserSubscription(models.Model):
    sub_id = models.ForeignKey(Subscription, max_length=200, on_delete=models.CASCADE, related_name='num_sub')
    name = models.CharField(max_length=15, default=False)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона.")],
        blank=True,
        null=True
    )
    date_arrive = models.DateField()
    address = models.TextField(blank=True)
    message = models.TextField(blank=True)
    schedule = models.IntegerField(default=0)
    type_tea = models.IntegerField(default=0)

    class Meta:
        verbose_name = ("UserSubscription")
        verbose_name_plural = ("UserSubscriptions")

# class User(AbstractUser):
#     email = models.EmailField(_("email address"), unique=True)
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_subscription = models.OneToOneField(UserSubscription, on_delete=models.CASCADE, null=True)
    subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.subscription}"