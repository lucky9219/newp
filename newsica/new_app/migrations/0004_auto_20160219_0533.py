# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 05:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0003_auto_20160215_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateField(default=datetime.date(2016, 2, 19)),
        ),
    ]
