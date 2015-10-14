# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20150831_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodeConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingSlice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='authority_hrn',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='created',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='login',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='status',
        ),
    ]
