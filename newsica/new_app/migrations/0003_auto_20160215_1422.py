# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0002_auto_20160215_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='news',
        ),
        migrations.RemoveField(
            model_name='user_news',
            name='user',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='user_news',
        ),
    ]
