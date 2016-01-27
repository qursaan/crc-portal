# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0038_auto_20160123_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='user_id',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
        migrations.AlterField(
            model_name='simreservation',
            name='user_id',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
    ]
