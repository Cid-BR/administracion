# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0006_auto_20170503_2322'),
        ('servicios', '0008_tiposervicio_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='factura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='facturas.Factura'),
        ),
    ]
