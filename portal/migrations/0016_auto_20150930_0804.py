# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_auto_20150920_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.TextField(null=True)),
                ('config', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BackendUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField(null=True)),
                ('keypair', models.TextField(null=True)),
                ('authority', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True)),
                ('longname', models.TextField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='Institution',
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
        migrations.AddField(
            model_name='account',
            name='platform_id',
            field=models.ForeignKey(to='portal.Platform', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.ForeignKey(to='portal.BackendUser', null=True),
        ),
    ]
