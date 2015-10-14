# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20150903_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 25267, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True)),
            ],
        ),
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
                ('created', models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 19109, tzinfo=utc))),
            ],
        ),
        migrations.DeleteModel(
            name='AccessLog',
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='authority_hrn',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 23478, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='number_of_nodes',
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='purpose',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='slice_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='type_of_nodes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendingslice',
            name='user_hrn',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='authority_hrn',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 14588, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='first_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='keypair',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='last_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='login',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='password',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='pi',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='approve_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 30537, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='reservation',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='image_id',
            field=models.ForeignKey(to='portal.Image', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='request_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 13, 47, 16, 30608, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='reservation',
            name='request_state',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_id',
            field=models.ForeignKey(to='portal.PendingUser', null=True),
        ),
        migrations.AddField(
            model_name='accesshistory',
            name='user_id',
            field=models.ForeignKey(to='portal.PendingUser', null=True),
        ),
        migrations.AddField(
            model_name='pendinguser',
            name='institeID',
            field=models.ForeignKey(to='portal.Institution', null=True),
        ),
    ]
