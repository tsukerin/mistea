# Generated by Django 4.2.5 on 2023-11-28 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0002_alter_tea_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='schedule',
            field=models.IntegerField(default=0),
        ),
    ]