# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0029_pendingslice_base_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pendingslice',
            old_name='type_of_nodes',
            new_name='server_type',
        ),
        migrations.AddField(
            model_name='myuser',
            name='active_email',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='request_type',
            field=models.TextField(default=b'NA'),
        ),
    ]
