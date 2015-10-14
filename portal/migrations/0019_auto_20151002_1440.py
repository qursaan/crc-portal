# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_auto_20151002_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='platform_id',
            new_name='platform_ref',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='user_id',
            new_name='user_ref',
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='user_hrn',
            field=models.TextField(null=True),
        ),
    ]
