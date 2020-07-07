# Generated by Django 3.0 on 2020-07-07 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_allproduct_instock'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='allproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='allproduct',
            name='unit',
            field=models.CharField(default='-', max_length=200),
        ),
    ]
