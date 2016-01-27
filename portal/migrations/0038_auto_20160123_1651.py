# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0037_auto_20160123_1632'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='myuserimage',
            name='user_ref',
        ),
        migrations.DeleteModel(
            name='MyUserImage',
        ),
    ]
