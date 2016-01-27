# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0024_pendingslice_slice_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.TextField(default=b'NA')),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodeDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.ForeignKey(to='portal.DeviceInfo', null=True)),
                ('node_id', models.ForeignKey(to='portal.Node', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='nodeconnection',
            name='node_dst',
            field=models.ForeignKey(related_name='des_node', to='portal.NodeDevice', null=True),
        ),
        migrations.AlterField(
            model_name='nodeconnection',
            name='node_src',
            field=models.ForeignKey(related_name='src_node', to='portal.NodeDevice', null=True),
        ),
    ]
