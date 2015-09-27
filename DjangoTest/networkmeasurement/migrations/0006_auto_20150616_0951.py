# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkmeasurement', '0005_remove_passive_jitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='active',
            name='createTime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passive',
            name='createTime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
