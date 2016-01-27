# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0033_auto_20160120_1457'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ResourceInfo',
            new_name='ResourcesInfo',
        ),
    ]
