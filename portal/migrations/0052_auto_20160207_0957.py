# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0051_auto_20160126_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simreservation',
            old_name='base_image_ref',
            new_name='image_ref',
        ),
        migrations.RenameField(
            model_name='simreservation',
            old_name='vm_ref',
            new_name='node_ref',
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='details',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='last_action',
            field=models.DateTimeField(null=True),
        ),
    ]
