# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='news',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='user_news',
        ),
    ]
