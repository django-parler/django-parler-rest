# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_code', models.CharField(unique=True, max_length=2, verbose_name='country code', db_index=True)),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('url', models.URLField(verbose_name='webpage', blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='testproj.Country', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'managed': True,
                'db_table': 'testproj_country_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'country Translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='countrytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
