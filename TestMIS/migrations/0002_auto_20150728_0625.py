# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excelcol',
            options={'ordering': ['sheet_name', 'col_pos_y'], 'verbose_name': 'Excel\u683c\u5f0f\u5b9a\u4e49', 'verbose_name_plural': 'Excel\u683c\u5f0f\u5b9a\u4e49\u5217\u8868'},
        ),
        migrations.AlterField(
            model_name='excelcol',
            name='sheet_name',
            field=models.CharField(help_text=b'excel\xe4\xb8\xadsheet\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97', max_length=21, verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84sheet'),
            preserve_default=True,
        ),
    ]
