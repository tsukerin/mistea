# Generated by Django 4.2.5 on 2023-12-07 10:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tea', '0003_remove_payment_subscription_remove_payment_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=False, max_length=15)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Введите корректный номер телефона.', regex='^\\+?1?\\d{9,15}$')])),
                ('date_arrive', models.DateField()),
                ('address', models.TextField(blank=True)),
                ('message', models.TextField(blank=True)),
                ('schedule', models.IntegerField(default=0)),
                ('type_tea', models.IntegerField(default=0)),
                ('sub_id', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, related_name='num_sub', to='tea.subscription')),
            ],
            options={
                'verbose_name': 'UserSubscription',
                'verbose_name_plural': 'UserSubscriptions',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('subscription', models.BooleanField(default=False)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile_address', to='user.usersubscription')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile_name', to='user.usersubscription')),
                ('phone_number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile_phone_number', to='user.usersubscription')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]