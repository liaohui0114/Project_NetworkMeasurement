# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkmeasurement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolnode',
            name='nodeIp',
            field=models.IPAddressField(),
            preserve_default=True,
        ),
    ]
