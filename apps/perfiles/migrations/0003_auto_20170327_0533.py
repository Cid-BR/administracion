# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 05:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0002_auto_20170327_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto',
            field=models.ImageField(default='img/avatar.png', upload_to='media/'),
        ),
    ]