# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0035_auto_20160121_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimReservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('f_start_time', models.DateTimeField(null=True)),
                ('f_end_time', models.DateTimeField(null=True)),
                ('slice_name', models.TextField(null=True)),
                ('slice_duration', models.TextField(default=b'1')),
                ('approve_date', models.DateTimeField(null=True)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_type', models.TextField(default=b'NA')),
                ('purpose', models.TextField(default=b'NA')),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('base_image', models.ForeignKey(to='portal.SimulationImage', null=True)),
                ('user_id', models.ForeignKey(to='portal.PendingUser', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationVM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vm_name', models.CharField(max_length=200, null=True)),
                ('specification', models.TextField(default=b'NA')),
            ],
        ),
        migrations.RemoveField(
            model_name='pendingreservationdetail',
            name='node_resource_id',
        ),
        migrations.RemoveField(
            model_name='pendingreservationdetail',
            name='slice_id',
        ),
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='node_resource_id',
            new_name='node_id',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='request_state',
        ),
        migrations.AddField(
            model_name='reservation',
            name='base_image',
            field=models.ForeignKey(to='portal.TestbedImage', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='f_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='f_start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='purpose',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='request_type',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='slice_duration',
            field=models.TextField(default=b'1'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='slice_name',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='PendingReservationDetail',
        ),
        migrations.AddField(
            model_name='simreservation',
            name='vm_name',
            field=models.ForeignKey(to='portal.SimulationVM', null=True),
        ),
    ]
