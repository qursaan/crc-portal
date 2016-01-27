# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0034_auto_20160121_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestbedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=200, null=True)),
                ('location', models.TextField(default=b'NA')),
                ('image_type', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='PendingSliceDetail',
            new_name='PendingReservationDetail',
        ),
        migrations.AlterField(
            model_name='reservationdetail',
            name='image_id',
            field=models.ForeignKey(to='portal.TestbedImage', null=True),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
