# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0041_auto_20160124_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vm_name', models.TextField(default=b'NA')),
                ('device_id', models.ForeignKey(to='portal.ResourcesInfo', null=True)),
                ('node_id', models.ForeignKey(to='portal.PhysicalNode', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='noderesource',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='noderesource',
            name='node_id',
        ),
        migrations.AlterField(
            model_name='nodeconnection',
            name='node_dst',
            field=models.ForeignKey(related_name='des_node', to='portal.VirtualNode', null=True),
        ),
        migrations.AlterField(
            model_name='nodeconnection',
            name='node_src',
            field=models.ForeignKey(related_name='src_node', to='portal.VirtualNode', null=True),
        ),
        migrations.AlterField(
            model_name='reservationdetail',
            name='node_id',
            field=models.ForeignKey(to='portal.VirtualNode', null=True),
        ),
        migrations.DeleteModel(
            name='NodeResource',
        ),
    ]
