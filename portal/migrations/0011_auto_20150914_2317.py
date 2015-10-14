# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20150913_2020'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PendingAuthority',
        ),
        migrations.RenameField(
            model_name='pendinguser',
            old_name='institeID',
            new_name='Institution',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='address_line3',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='address_postalcode',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='site_latitude',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='site_longitude',
        ),
    ]
