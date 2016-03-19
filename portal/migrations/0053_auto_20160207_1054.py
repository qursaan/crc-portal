# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0052_auto_20160207_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='simreservation',
            name='details',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='simreservation',
            name='last_action',
            field=models.DateTimeField(null=True),
        ),
    ]
