# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkmeasurement', '0003_auto_20150614_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('bandwidth', models.FloatField(default=0)),
                ('throughput', models.FloatField(default=0)),
                ('jitter', models.FloatField(default=0)),
                ('loss', models.FloatField(default=0)),
                ('rtt', models.FloatField(default=0)),
                ('cpu', models.FloatField(default=0)),
                ('memory', models.FloatField(default=0)),
                ('endNode', models.ForeignKey(related_name='passive_end_node', to='networkmeasurement.SchoolNode')),
                ('startNode', models.ForeignKey(related_name='passive_start_node', to='networkmeasurement.SchoolNode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='active',
            name='bandwidth',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='active',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='active',
            name='delay',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='active',
            name='jitter',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='active',
            name='loss',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
