# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190123_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='head',
            field=models.ImageField(default='head/qqlogin.png', upload_to='shop/%Y%m/%d'),
        ),
    ]