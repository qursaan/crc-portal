# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0045_auto_20160124_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationvm',
            name='hv_name',
            field=models.TextField(default=b'NA', verbose_name=b'Hypervisor Name'),
        ),
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
        migrations.AlterField(
            model_name='simulationvm',
            name='vm_name',
            field=models.TextField(default=b'NA', verbose_name=b'Virtual Node Name'),
        ),
    ]
