# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0040_auto_20160124_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('num_interface', models.IntegerField(default=0)),
                ('num_virtual', models.IntegerField(default=0)),
                ('num_connection', models.IntegerField(default=0)),
                ('node_ip', models.TextField(default=b'NA')),
            ],
        ),
        migrations.AlterField(
            model_name='noderesource',
            name='node_id',
            field=models.ForeignKey(to='portal.PhysicalNode', null=True),
        ),
        migrations.DeleteModel(
            name='Node',
        ),
    ]
