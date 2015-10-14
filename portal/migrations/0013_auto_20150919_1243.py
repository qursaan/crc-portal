# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_pendingauthority'),
    ]

    operations = [
        migrations.AddField(
            model_name='authority',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='pendingauthority',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
