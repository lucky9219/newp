# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-26 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0013_auto_20160226_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_news',
            name='upload',
            field=models.FileField(upload_to=b'static/img/usruploads/'),
        ),
    ]
