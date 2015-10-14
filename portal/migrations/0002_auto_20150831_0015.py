# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingusers',
            name='authority_hrn',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pendingusers',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pendingusers',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pendingusers',
            name='login',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pendingusers',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
