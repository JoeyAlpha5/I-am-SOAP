# Generated by Django 2.1.1 on 2019-01-08 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_order_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.TextField(default=''),
        ),
    ]
