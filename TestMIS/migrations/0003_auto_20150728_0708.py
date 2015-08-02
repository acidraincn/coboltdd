# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0002_auto_20150728_0625'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='excelcol',
            unique_together=set([('sheet_name', 'col_pos_y')]),
        ),
    ]
