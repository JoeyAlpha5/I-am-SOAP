# Generated by Django 2.1.1 on 2018-12-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='img',
            new_name='ig',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='products'),
            preserve_default=False,
        ),
    ]