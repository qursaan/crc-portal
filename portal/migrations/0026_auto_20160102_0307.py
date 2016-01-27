# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0025_auto_20160102_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='num_connect',
            new_name='num_connection',
        ),
        migrations.RenameField(
            model_name='node',
            old_name='num_intface',
            new_name='num_interface',
        ),
    ]
