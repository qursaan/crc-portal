# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0046_auto_20160125_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesshistory',
            old_name='user_id',
            new_name='user_ref',
        ),
        migrations.RenameField(
            model_name='nodeconnection',
            old_name='node_dst',
            new_name='node_dst_ref',
        ),
        migrations.RenameField(
            model_name='nodeconnection',
            old_name='node_src',
            new_name='node_src_ref',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='base_image',
            new_name='base_image_ref',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='user_id',
            new_name='user_ref',
        ),
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='image_id',
            new_name='image_ref',
        ),
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='node_id',
            new_name='node_ref',
        ),
        migrations.RenameField(
            model_name='reservationdetail',
            old_name='reservation_id',
            new_name='reservation_ref',
        ),
        migrations.RenameField(
            model_name='simreservation',
            old_name='user_id',
            new_name='user_ref',
        ),
        migrations.RenameField(
            model_name='virtualnode',
            old_name='device_id',
            new_name='device_ref',
        ),
        migrations.RenameField(
            model_name='virtualnode',
            old_name='node_id',
            new_name='node_ref',
        ),
    ]
