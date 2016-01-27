# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0036_auto_20160123_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='f_end_time',
            field=models.DateTimeField(null=True, verbose_name=b'Fixable End Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='f_start_time',
            field=models.DateTimeField(null=True, verbose_name=b'Fixable Start Time'),
        ),
    ]
