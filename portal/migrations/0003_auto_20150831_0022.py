# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20150831_0015'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PendingUsers',
            new_name='PendingUser',
        ),
    ]
