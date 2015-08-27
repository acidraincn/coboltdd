# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0006_auto_20150730_0722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excelcontraint',
            name='excel_col',
        ),
        migrations.AddField(
            model_name='excelcontraint',
            name='relative_constraint',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xbe\x9d\xe8\xb5\x96\xe7\xba\xa6\xe6\x9d\x9f', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='excelcontraint',
            name='relative_from',
            field=models.ForeignKey(related_name='dependency col', verbose_name=b'\xe4\xbe\x9d\xe8\xb5\x96\xe5\x88\x97', blank=True, to='TestMIS.ExcelCol', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='excelcontraint',
            name='relative_value',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xbe\x9d\xe8\xb5\x96\xe5\x88\x97\xe7\x9a\x84\xe5\x8f\x96\xe5\x80\xbc', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excelcontraint',
            name='constraint_type',
            field=models.CharField(max_length=1, verbose_name=b'\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'R', b'\xe6\xad\xa3\xe5\x88\x99\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f'), (b'L', b'\xe5\x88\x97\xe8\xa1\xa8'), (b'C', b'COBOL\xe5\xad\x90\xe5\x8f\xa5'), (b'S', b'\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe6\x9c\x89\xe7\xa9\xba\xe6\xa0\xbc'), (b'O', b'\xe9\x9d\x9e\xe7\xa9\xba\xe5\x80\xbc'), (b'X', b'\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x80\xbc'), (b'N', b'\xe5\x85\x81\xe8\xae\xb8\xe7\xa9\xba\xe5\x80\xbc'), (b'M', b'\xe5\x85\xb3\xe8\x81\x94\xe7\xba\xa6\xe6\x9d\x9f')]),
            preserve_default=True,
        ),
    ]
