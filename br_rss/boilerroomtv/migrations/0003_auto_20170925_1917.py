# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boilerroomtv', '0002_channel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'ordering': ('id',)},
        ),
    ]
