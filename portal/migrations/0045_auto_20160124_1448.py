# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0044_myuser_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='login',
            new_name='username',
        ),
    ]
