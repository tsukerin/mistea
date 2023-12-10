from datetime import datetime
from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

#Категории чая
class TeaCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('shop:tea_list_by_category', args=[self.slug])  

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория чая'
        verbose_name_plural = 'Категории чая'

    def __str__(self):
        return self.name
#Подписка
class Subscription(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    teas = models.ManyToManyField('Tea', related_name='subscriptions', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='subscription_images/', default="images/flowers.jpeg")
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка на чай'
        verbose_name_plural = 'Подписки на чай'

    def __str__(self):
        return self.name
    
class Tea(models.Model):
    category = models.ForeignKey(TeaCategory, related_name='teas', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='teas/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('shop:tea_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name