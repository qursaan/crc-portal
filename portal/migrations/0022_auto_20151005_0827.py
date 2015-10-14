# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0021_myuserimage_node_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuserimage',
            name='node_num',
        ),
        migrations.AlterField(
            model_name='myuserimage',
            name='image_name',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
