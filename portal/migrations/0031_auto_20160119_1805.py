# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0030_auto_20160119_0347'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NodeDevice',
            new_name='NodeResource',
        ),
        migrations.RenameModel(
            old_name='DeviceInfo',
            new_name='ResourceInfo',
        ),
    ]
