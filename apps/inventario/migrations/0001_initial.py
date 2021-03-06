# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio_compra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('existencias', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Articulos')),
            ],
        ),
    ]
