# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0007_auto_20150803_0153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='excelcontraint',
            name='excel_col',
            field=models.ForeignKey(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe7\xba\xa6\xe6\x9d\x9f\xe7\x9a\x84\xe5\x88\x97', to='TestMIS.ExcelCol', null=True),
            preserve_default=True,
        ),
    ]
