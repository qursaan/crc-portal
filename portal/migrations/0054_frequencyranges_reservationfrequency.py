# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0053_auto_20160207_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequencyRanges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.TextField(null=True)),
                ('freq_start', models.TextField(null=True)),
                ('freq_end', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency_ref', models.ForeignKey(to='portal.FrequencyRanges', null=True)),
                ('reservation_ref', models.ForeignKey(to='portal.Reservation', null=True)),
            ],
        ),
    ]
