# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkmeasurement', '0002_auto_20150506_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createTime', models.DateTimeField()),
                ('bandwidth', models.FloatField()),
                ('delay', models.FloatField()),
                ('jitter', models.FloatField()),
                ('loss', models.FloatField()),
                ('congestion', models.BooleanField(default=False)),
                ('avail', models.BooleanField(default=False)),
                ('endNode', models.ForeignKey(related_name='end_node', to='networkmeasurement.SchoolNode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetProtocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocolName', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='active',
            name='protocol',
            field=models.ForeignKey(to='networkmeasurement.NetProtocol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='active',
            name='startNode',
            field=models.ForeignKey(related_name='start_node', to='networkmeasurement.SchoolNode'),
            preserve_default=True,
        ),
    ]
