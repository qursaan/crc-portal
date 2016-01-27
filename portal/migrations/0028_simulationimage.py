# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0027_auto_20160102_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulationImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('image_type', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
