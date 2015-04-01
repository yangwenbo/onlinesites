# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package', models.CharField(max_length=30)),
                ('md5hash', models.CharField(max_length=50)),
                ('upload_location', models.TextField()),
                ('static_location', models.TextField()),
                ('dynamic_location', models.TextField()),
                ('download_location', models.TextField()),
                ('upload_time', models.DateTimeField()),
                ('static_time', models.DateTimeField()),
                ('dynamic_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
