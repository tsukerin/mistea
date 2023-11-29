from datetime import datetime
from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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
    # Связь с чаями, входящими в подписку
    teas = models.ManyToManyField('Tea', related_name='subscriptions', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='subscription_images/', default="images/flowers.jpeg")
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка на чай'
        verbose_name_plural = 'Подписки на чай'

    def __str__(self):
        return self.name
    
class UserSubscription(models.Model):
    sub_id = models.ForeignKey(Subscription, max_length=200, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("UserSubscription_detail", kwargs={"pk": self.pk})

#----------------------------------------------------------------------------------------------------------------------------------
# пользователь
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='userprofile_name', null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='userprofile_address', null=True)
    subscription = models.BooleanField(default=False)
    phone_number = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='userprofile_phone_number', null=True)




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

#отзывы
class Review(models.Model):
    tea = models.ForeignKey('Tea', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

#Заказ
class Order(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    tea = models.ForeignKey('Tea', on_delete=models.CASCADE)
    delivery_interval = models.CharField(max_length=255, choices=[("monthly", "Ежемесячно"), ("quarterly", "Каждые 3 месяца")])
    tea_format = models.CharField(max_length=255, choices=[("tea_bags", "Пакетики"), ("loose_leaf", "Листовой чай")])
    delivery_address = models.TextField()
    status = models.CharField(max_length=255, choices=[("processing", "Обработка"), ("shipped", "Отправлено"), ("delivered", "Доставлено")])
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, choices=[("credit_card", "Кредитная карта"), ("paypal", "PayPal"), ("other", "Другой")])
    payment_status = models.CharField(max_length=255, choices=[("pending", "Ожидает оплаты"), ("paid", "Оплачено")])

#платеж
class Payment(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, choices=[("credit_card", "Кредитная карта"), ("paypal", "PayPal"), ("other", "Другой")])
    payment_status = models.CharField(max_length=255, choices=[("pending", "Ожидает оплаты"), ("paid", "Оплачено")])
    recurring = models.BooleanField(default=False)
    recurring_interval = models.CharField(max_length=255, choices=[("monthly", "Ежемесячно"), ("quarterly", "Каждые 3 месяца")], blank=True, null=True)