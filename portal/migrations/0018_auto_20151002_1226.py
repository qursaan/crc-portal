# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_auto_20151001_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='approved_by',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_hrn',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='slice',
            name='approve_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='slice',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='slice',
            name='request_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='slice',
            name='request_state',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='slice',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='slice',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='accesshistory',
            name='user_id',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
    ]
