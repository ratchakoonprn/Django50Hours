# Generated by Django 3.0 on 2020-08-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_cart_stamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cartquan',
            field=models.IntegerField(default=0),
        ),
    ]
