# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0026_auto_20160102_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='description',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AlterField(
            model_name='nodeconnection',
            name='description',
            field=models.TextField(default=b'NA'),
        ),
    ]
