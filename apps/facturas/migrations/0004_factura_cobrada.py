# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0003_factura_facturaitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='cobrada',
            field=models.BooleanField(default=False),
        ),
    ]
