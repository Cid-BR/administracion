# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20170428_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('direccion', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=30)),
                ('telefono2', models.CharField(max_length=30)),
                ('valoracion', models.CharField(blank=True, choices=[('Excelente', 'excelente'), ('Muy bueno', 'muy_bueno'), ('Bueno', 'bueno'), ('Regular', 'regular'), ('Deficiente', 'deficiente'), ('Malo', 'malo'), ('Muy malo', 'muy_malo')], default='estado_pendiente', max_length=50, null=True)),
            ],
        ),
    ]
