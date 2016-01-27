# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0023_myuserimage_image_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingslice',
            name='slice_duration',
            field=models.TextField(default=b'1'),
        ),
    ]
