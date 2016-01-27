# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0049_auto_20160126_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='end_day',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='f_end_day',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='f_start_day',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='start_day',
        ),
    ]
