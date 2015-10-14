# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20150903_0422'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Access',
            new_name='AccessLog',
        ),
    ]
