# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.TextField(null=True)),
                ('config', models.TextField(null=True)),
            ],
        ),
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
                ('address_city', models.TextField(null=True)),
                ('address_state', models.TextField(null=True)),
                ('address_country', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
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
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('username', models.TextField(null=True)),
                ('password', models.TextField(null=True)),
                ('keypair', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('user_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_by', models.TextField(null=True)),
                ('status', models.IntegerField(default=0, null=True)),
                ('active_email', models.IntegerField(default=0, null=True)),
                ('is_admin', models.IntegerField(default=0, null=True)),
                ('user_type', models.IntegerField(default=0, null=True)),
                ('supervisor_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NodeConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=b'NA')),
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
                ('address_city', models.TextField(null=True)),
                ('address_state', models.TextField(null=True)),
                ('address_country', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingSlice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slice_name', models.TextField(null=True)),
                ('user_hrn', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('number_of_nodes', models.TextField(default=0)),
                ('server_type', models.TextField(default=b'NA')),
                ('request_type', models.TextField(default=b'NA')),
                ('base_image', models.TextField(default=b'NA')),
                ('purpose', models.TextField(default=b'NA')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('slice_duration', models.TextField(default=b'1')),
                ('status', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('request_date', models.DateTimeField(null=True)),
                ('approve_date', models.DateTimeField(null=True)),
                ('request_state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PendingUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField(null=True)),
                ('keypair', models.TextField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('login', models.TextField(null=True)),
                ('user_hrn', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('num_interface', models.IntegerField(default=0)),
                ('num_virtual', models.IntegerField(default=0)),
                ('num_connection', models.IntegerField(default=0)),
                ('node_ip', models.TextField(default=b'NA')),
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
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('start_time', models.DateTimeField(null=True, verbose_name=b'Actual Start Time')),
                ('end_time', models.DateTimeField(null=True, verbose_name=b'Actual End Time')),
                ('f_start_time', models.DateTimeField(null=True, verbose_name=b'Estimate Start Time')),
                ('f_end_time', models.DateTimeField(null=True, verbose_name=b'Estimate End Time')),
                ('slice_name', models.TextField(null=True)),
                ('slice_duration', models.TextField(default=b'1')),
                ('approve_date', models.DateTimeField(null=True)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_type', models.TextField(default=b'NA')),
                ('purpose', models.TextField(default=b'NA')),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_action', models.DateTimeField(null=True)),
                ('details', models.TextField(default=b'NA')),
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
        migrations.CreateModel(
            name='ResourcesInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.TextField(default=b'NA')),
                ('description', models.TextField(default=b'NA')),
            ],
        ),
        migrations.CreateModel(
            name='SimReservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('authority_hrn', models.TextField(null=True)),
                ('f_start_time', models.DateTimeField(null=True)),
                ('f_end_time', models.DateTimeField(null=True)),
                ('slice_name', models.TextField(null=True)),
                ('slice_duration', models.TextField(default=b'1')),
                ('approve_date', models.DateTimeField(null=True)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_type', models.TextField(default=b'NA')),
                ('n_processor', models.IntegerField(default=1)),
                ('n_ram', models.IntegerField(default=1024)),
                ('purpose', models.TextField(default=b'NA')),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_action', models.DateTimeField(null=True)),
                ('details', models.TextField(default=b'NA')),
            ],
        ),
        migrations.CreateModel(
            name='SimulationImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('image_type', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationVM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vm_name', models.TextField(default=b'NA', verbose_name=b'Virtual Node Name')),
                ('hv_name', models.TextField(default=b'NA', verbose_name=b'Hypervisor Name')),
                ('specification', models.TextField(default=b'NA')),
            ],
        ),
        migrations.CreateModel(
            name='TestbedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('image_type', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=300, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('image_type', models.CharField(max_length=200, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_load', models.DateTimeField(null=True)),
                ('user_ref', models.ForeignKey(to='portal.MyUser', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vm_name', models.TextField(default=b'NA', verbose_name=b'Virtual Node Name')),
                ('hv_name', models.TextField(default=b'NA', verbose_name=b'Hypervisor Name')),
                ('device_ref', models.ForeignKey(to='portal.ResourcesInfo', null=True)),
                ('node_ref', models.ForeignKey(to='portal.PhysicalNode', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='simreservation',
            name='image_ref',
            field=models.ForeignKey(to='portal.SimulationImage', null=True),
        ),
        migrations.AddField(
            model_name='simreservation',
            name='node_ref',
            field=models.ForeignKey(to='portal.SimulationVM', null=True),
        ),
        migrations.AddField(
            model_name='simreservation',
            name='user_ref',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='image_ref',
            field=models.ForeignKey(to='portal.TestbedImage', null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='node_ref',
            field=models.ForeignKey(to='portal.VirtualNode', null=True),
        ),
        migrations.AddField(
            model_name='reservationdetail',
            name='reservation_ref',
            field=models.ForeignKey(to='portal.Reservation', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='base_image_ref',
            field=models.ForeignKey(to='portal.TestbedImage', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_ref',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
        migrations.AddField(
            model_name='nodeconnection',
            name='node_dst_ref',
            field=models.ForeignKey(related_name='des_node', to='portal.VirtualNode', null=True),
        ),
        migrations.AddField(
            model_name='nodeconnection',
            name='node_src_ref',
            field=models.ForeignKey(related_name='src_node', to='portal.VirtualNode', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='platform_ref',
            field=models.ForeignKey(to='portal.Platform', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='user_ref',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
        migrations.AddField(
            model_name='accesshistory',
            name='user_ref',
            field=models.ForeignKey(to='portal.MyUser', null=True),
        ),
    ]
