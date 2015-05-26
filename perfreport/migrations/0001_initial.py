# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import perfreport.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PerfCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the case, 128 characters allowed', unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PerfRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_mem_consumption', models.FloatField(help_text=b'Total Memory Consumption, in GB*Hours')),
                ('peak_host_mem', models.FloatField(help_text=b'Peak Host Memory, in GB')),
                ('overall_runtime', models.IntegerField(help_text=b'Overall Running Time, in seconds')),
                ('highest_cmd_mem', models.FloatField(help_text=b'Highest Command Memory, in MB')),
                ('peak_disk', models.FloatField(help_text=b'Peak Disk Usage, in Mb')),
                ('case', models.ForeignKey(to='perfreport.PerfCase')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'dev', help_text=b'Releases in format of YYYY.MM (with or without -SPn) or dev, default is dev', unique=True, max_length=11, validators=[perfreport.models.validate_release])),
            ],
        ),
        migrations.CreateModel(
            name='Suite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the suite, 128 characters allowed', unique=True, max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='perfrecord',
            name='rel_ver',
            field=models.ForeignKey(to='perfreport.Release'),
        ),
        migrations.AddField(
            model_name='perfcase',
            name='suite',
            field=models.ForeignKey(to='perfreport.Suite'),
        ),
    ]
