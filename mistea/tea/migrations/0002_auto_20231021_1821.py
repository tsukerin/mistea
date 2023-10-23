# Generated by Django 3.2.10 on 2023-10-21 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tea.subscription')),
                ('tea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.tea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Кредитная карта'), ('paypal', 'PayPal'), ('other', 'Другой')], max_length=255)),
                ('payment_status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('paid', 'Оплачено')], max_length=255)),
                ('recurring', models.BooleanField(default=False)),
                ('recurring_interval', models.CharField(blank=True, choices=[('monthly', 'Ежемесячно'), ('quarterly', 'Каждые 3 месяца')], max_length=255, null=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_interval', models.CharField(choices=[('monthly', 'Ежемесячно'), ('quarterly', 'Каждые 3 месяца')], max_length=255)),
                ('tea_format', models.CharField(choices=[('tea_bags', 'Пакетики'), ('loose_leaf', 'Листовой чай')], max_length=255)),
                ('delivery_address', models.TextField()),
                ('status', models.CharField(choices=[('processing', 'Обработка'), ('shipped', 'Отправлено'), ('delivered', 'Доставлено')], max_length=255)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Кредитная карта'), ('paypal', 'PayPal'), ('other', 'Другой')], max_length=255)),
                ('payment_status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('paid', 'Оплачено')], max_length=255)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.subscription')),
                ('tea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.tea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.userprofile')),
            ],
        ),
    ]