# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('web_url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('artists', models.CharField(max_length=300)),
                ('released', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('thumbnail_url', models.URLField(blank=True)),
                ('audio_url', models.URLField()),
                ('audio_content_type', models.CharField(max_length=200)),
                ('audio_content_length', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('-released',),
            },
        ),
    ]
