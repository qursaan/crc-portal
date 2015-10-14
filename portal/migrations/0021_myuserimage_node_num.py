# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_auto_20151005_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuserimage',
            name='node_num',
            field=models.TextField(default=b'NA'),
        ),
    ]
