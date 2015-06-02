# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import perfreport.models


class Migration(migrations.Migration):

    dependencies = [
        ('perfreport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfcase',
            name='run_modes',
            field=models.ManyToManyField(to='perfreport.RunMode', blank=True),
        ),
        migrations.AlterField(
            model_name='runmode',
            name='name',
            field=models.CharField(help_text=b'Running mode in format of DPxxTHxx or DPxxTL', unique=True, max_length=8, validators=[perfreport.models.validate_runmode]),
        ),
    ]
