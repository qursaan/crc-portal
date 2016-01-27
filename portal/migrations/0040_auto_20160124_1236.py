# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0039_auto_20160124_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='authority_hrn',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='simreservation',
            name='authority_hrn',
            field=models.TextField(null=True),
        ),
    ]
