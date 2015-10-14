# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_auto_20150920_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='image_id',
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='approve_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='request_state',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='image_id',
            field=models.ForeignKey(to='portal.Image', null=True),
        ),
    ]
