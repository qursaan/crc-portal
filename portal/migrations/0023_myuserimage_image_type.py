# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0022_auto_20151005_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuserimage',
            name='image_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
