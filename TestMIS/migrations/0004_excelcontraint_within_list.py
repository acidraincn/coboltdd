# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('TestMIS', '0003_auto_20150728_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='excelcontraint',
            name='within_list',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex=b'(\\S+?, \xef\xbc\x9f)+')], max_length=200, blank=True, help_text=b'\xe4\xbb\x85\xe5\xbd\x93\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b\xe9\x80\x89\xe6\x8b\xa9\xe2\x80\x9c\xe5\x88\x97\xe8\xa1\xa8\xe2\x80\x9d\xe6\x97\xb6\xe6\x9c\x89\xe6\x95\x88', null=True, verbose_name=b'\xe6\x9e\x9a\xe4\xb8\xbe\xe5\x88\x97\xe8\xa1\xa8'),
            preserve_default=True,
        ),
    ]
