# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20170208_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='minimo_existencias',
            field=models.IntegerField(default=1),
        ),
    ]
