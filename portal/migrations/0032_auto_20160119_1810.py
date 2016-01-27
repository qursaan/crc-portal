# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0031_auto_20160119_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationdetail',
            name='node_id',
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='node_resource_id',
            field=models.ForeignKey(to='portal.NodeResource', null=True),
        ),
    ]
