# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0047_auto_20160126_0644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simreservation',
            old_name='base_image',
            new_name='base_image_ref',
        ),
        migrations.RenameField(
            model_name='simreservation',
            old_name='vm_name',
            new_name='vm_ref',
        ),
    ]
