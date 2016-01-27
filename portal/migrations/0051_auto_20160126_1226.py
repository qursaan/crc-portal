# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0050_auto_20160126_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name=b'Actual End Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='f_end_time',
            field=models.DateTimeField(null=True, verbose_name=b'Estimate End Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='f_start_time',
            field=models.DateTimeField(null=True, verbose_name=b'Estimate Start Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name=b'Actual Start Time'),
        ),
    ]
