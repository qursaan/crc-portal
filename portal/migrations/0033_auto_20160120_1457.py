# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0032_auto_20160119_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingSliceDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_resource_id', models.ForeignKey(to='portal.NodeResource', null=True)),
                ('slice_id', models.ForeignKey(to='portal.PendingSlice', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
