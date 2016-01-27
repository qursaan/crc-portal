# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0043_auto_20160124_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='login',
            field=models.TextField(null=True),
        ),
    ]
