# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0048_auto_20160126_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='end_day',
            field=models.DateField(null=True, verbose_name=b'Actual End Day'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='f_end_day',
            field=models.DateField(null=True, verbose_name=b'Estimate End Day'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='f_start_day',
            field=models.DateField(null=True, verbose_name=b'Estimate Start Day'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_day',
            field=models.DateField(null=True, verbose_name=b'Actual Start Day'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(null=True, verbose_name=b'Actual End Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='f_end_time',
            field=models.TimeField(null=True, verbose_name=b'Estimate End Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='f_start_time',
            field=models.TimeField(null=True, verbose_name=b'Estimate Start Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(null=True, verbose_name=b'Actual Start Time'),
        ),
    ]
