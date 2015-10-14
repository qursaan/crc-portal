# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20151002_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUserImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_load', models.DateTimeField(null=True)),
                ('user_ref', models.ForeignKey(to='portal.MyUser', null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Slice',
        ),
    ]
