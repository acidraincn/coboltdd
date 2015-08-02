# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0005_auto_20150728_0733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excelcol',
            options={'ordering': ['sheet_name', 'col_pos_x'], 'verbose_name': 'Excel\u683c\u5f0f\u5b9a\u4e49', 'verbose_name_plural': 'Excel\u683c\u5f0f\u5b9a\u4e49\u5217\u8868'},
        ),
        migrations.RenameField(
            model_name='excelcol',
            old_name='col_pos_y',
            new_name='col_pos_x',
        ),
        migrations.AlterField(
            model_name='excelcol',
            name='sheet_name',
            field=models.CharField(default=b'\xe5\x8d\x95\xe5\x85\x83\xe6\xb5\x8b\xe8\xaf\x95\xe5\x88\x86\xe6\x9e\x90', help_text=b'excel\xe4\xb8\xadsheet\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97', max_length=21, verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84sheet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excelcontraint',
            name='constraint_type',
            field=models.CharField(max_length=1, verbose_name=b'\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'R', b'\xe6\xad\xa3\xe5\x88\x99\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f'), (b'L', b'\xe5\x88\x97\xe8\xa1\xa8'), (b'C', b'COBOL\xe5\xad\x90\xe5\x8f\xa5'), (b'S', b'\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe6\x9c\x89\xe7\xa9\xba\xe6\xa0\xbc'), (b'O', b'\xe9\x9d\x9e\xe7\xa9\xba\xe5\x80\xbc'), (b'X', b'\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x80\xbc'), (b'N', b'\xe5\x85\x81\xe8\xae\xb8\xe7\xa9\xba\xe5\x80\xbc')]),
            preserve_default=True,
        ),
    ]
