# Generated by Django 4.2.5 on 2023-11-26 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0003_subscription_image_alter_subscription_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscription',
            field=models.BooleanField(default=False),
        ),
    ]