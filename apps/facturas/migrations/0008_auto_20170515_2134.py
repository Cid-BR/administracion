# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0007_auto_20170514_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]