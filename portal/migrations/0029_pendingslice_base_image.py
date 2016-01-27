# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0028_simulationimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingslice',
            name='base_image',
            field=models.TextField(default=b'NA'),
        ),
    ]
