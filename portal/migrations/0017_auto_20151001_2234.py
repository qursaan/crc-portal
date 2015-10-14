# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0016_auto_20150930_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField(null=True)),
                ('keypair', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(default=0, null=True)),
                ('is_admin', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pendingauthority',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='pendingauthority',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='pendingauthority',
            name='address_line3',
        ),
        migrations.RemoveField(
            model_name='pendingauthority',
            name='address_postalcode',
        ),
        migrations.RemoveField(
            model_name='pendinguser',
            name='pi',
        ),
        migrations.AddField(
            model_name='authority',
            name='site_latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='site_longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='request_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_id',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
        migrations.DeleteModel(
            name='BackendUser',
        ),
    ]
