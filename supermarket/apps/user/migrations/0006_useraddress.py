# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 21:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190123_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='收货人')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '电话号码格式错误')], verbose_name='收货人电话')),
                ('hcity', models.CharField(blank=True, max_length=100, null=True, verbose_name='省')),
                ('hproper', models.CharField(blank=True, max_length=100, null=True, verbose_name='市')),
                ('harea', models.CharField(max_length=100, verbose_name='区')),
                ('brief', models.CharField(max_length=255, verbose_name='详细地址')),
                ('isDefault', models.BooleanField(default=False, verbose_name='是否设置为默认')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Users', verbose_name='创建人')),
            ],
            options={
                'verbose_name': '收货地址管理',
                'verbose_name_plural': '收货地址管理',
            },
        ),
    ]