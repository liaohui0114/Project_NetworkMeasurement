# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkmeasurement', '0006_auto_20150616_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='passive',
            name='ip_bandwidth',
            field=models.IPAddressField(default=b'127.0.0.1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passive',
            name='ip_cpu',
            field=models.IPAddressField(default=b'127.0.0.1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passive',
            name='ip_memory',
            field=models.IPAddressField(default=b'127.0.0.1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passive',
            name='ip_throughput',
            field=models.IPAddressField(default=b'127.0.0.1'),
            preserve_default=True,
        ),
    ]
