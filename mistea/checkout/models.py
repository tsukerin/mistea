from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False)
