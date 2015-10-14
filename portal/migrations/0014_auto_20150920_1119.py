# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20150919_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingslice',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pendingslice',
            name='purpose',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AlterField(
            model_name='pendingslice',
            name='type_of_nodes',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AlterField(
            model_name='slice',
            name='purpose',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AlterField(
            model_name='slice',
            name='type_of_nodes',
            field=models.TextField(default=b'NA'),
        ),
    ]
