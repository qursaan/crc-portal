# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_auto_20150914_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingAuthority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.TextField(null=True)),
                ('site_authority', models.TextField(null=True)),
                ('site_abbreviated_name', models.TextField(null=True)),
                ('site_url', models.TextField(null=True)),
                ('site_latitude', models.TextField(null=True)),
                ('site_longitude', models.TextField(null=True)),
                ('address_line1', models.TextField(null=True)),
                ('address_line2', models.TextField(null=True)),
                ('address_line3', models.TextField(null=True)),
                ('address_city', models.TextField(null=True)),
                ('address_postalcode', models.TextField(null=True)),
                ('address_state', models.TextField(null=True)),
                ('address_country', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
