# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0004_factura_contado'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='fecha_limite',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
