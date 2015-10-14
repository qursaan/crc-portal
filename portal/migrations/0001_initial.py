# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('authority_hrn', models.TextField()),
                ('login', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
