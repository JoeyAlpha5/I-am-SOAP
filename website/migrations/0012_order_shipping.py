# Generated by Django 2.1.1 on 2019-01-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_order_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.BooleanField(default=False),
        ),
    ]
