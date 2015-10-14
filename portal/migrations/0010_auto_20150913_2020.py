# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20150910_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
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
        migrations.CreateModel(
            name='Slice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slice_name', models.TextField(null=True)),
                ('user_hrn', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('number_of_nodes', models.TextField(default=0)),
                ('type_of_nodes', models.TextField(null=True)),
                ('purpose', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='image_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='image_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='node',
            name='location',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='node_ip',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='node',
            name='node_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='num_connect',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='num_intface',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='num_virtual',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nodeconnection',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='nodeconnection',
            name='node_dst',
            field=models.ForeignKey(related_name='des_node', to='portal.Node', null=True),
        ),
        migrations.AddField(
            model_name='nodeconnection',
            name='node_src',
            field=models.ForeignKey(related_name='src_node', to='portal.Node', null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='node_id',
            field=models.ForeignKey(to='portal.Node', null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='reservation_id',
            field=models.ForeignKey(to='portal.Reservation', null=True),
        ),
    ]
