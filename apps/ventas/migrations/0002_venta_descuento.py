# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='descuento',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]