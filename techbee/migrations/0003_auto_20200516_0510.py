# Generated by Django 2.2.10 on 2020-05-16 05:10

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techbee', '0002_auto_20200516_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_meta',
            name='photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]