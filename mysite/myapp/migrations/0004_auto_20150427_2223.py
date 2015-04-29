# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20150324_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='dynamic_status',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sample',
            name='static_status',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
