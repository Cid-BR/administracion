# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0003_egresos_aprovado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresos',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
