from django.db import models

class TeaCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория чая'
        verbose_name_plural = 'Категории чая'

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    
    # Связь с чаями, входящими в подписку
    teas = models.ManyToManyField('tea', related_name='subscriptions', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка на чай'
        verbose_name_plural = 'Подписки на чай'

    def __str__(self):
        return self.name

class Tea(models.Model):
    category = models.ForeignKey(TeaCategory, related_name='Чаи', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='teas/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
