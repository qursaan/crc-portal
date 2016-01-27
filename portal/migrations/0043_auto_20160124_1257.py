# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0042_auto_20160124_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualnode',
            name='hv_name',
            field=models.TextField(default=b'NA', verbose_name=b'Hypervisor Name'),
        ),
        migrations.AlterField(
            model_name='virtualnode',
            name='vm_name',
            field=models.TextField(default=b'NA', verbose_name=b'Virtual Node Name'),
        ),
    ]
