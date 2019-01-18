# Generated by Django 2.1.1 on 2018-11-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Bars', 'Bars'), ('Shaving', 'Shaving'), ('Oil', 'Oil'), ('Shampoo', 'Shampoo'), ('Salts', 'Salts'), ('Cream', 'Cream')], default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
