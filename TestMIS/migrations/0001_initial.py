# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelCol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sheet_name', models.CharField(help_text=b'excel\xe4\xb8\xadsheet\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97', max_length=21, verbose_name=b'Sheet Name')),
                ('col_name', models.CharField(help_text=b'\xe7\xbb\x84\xe6\x88\x90\xe6\xb5\x8b\xe8\xaf\x95\xe5\x88\x86\xe6\x9e\x90or\xe6\xa1\x88\xe4\xbe\x8b\xe6\x89\x80\xe5\xbf\x85\xe8\xa6\x81\xe7\x9a\x84\xe5\x88\x97', max_length=20, verbose_name=b'\xe5\x88\x97\xe5\x90\x8d')),
                ('col_pos_y', models.IntegerField(help_text=b'\xe6\x9c\xac\xe5\x88\x97\xe5\x9c\xa8\xe8\xa7\x84\xe5\xae\x9a\xe7\x9a\x84excel\xe6\xa0\xbc\xe5\xbc\x8f\xe8\xa6\x81\xe6\xb1\x82\xe5\x86\x85\xe7\x9a\x84\xe5\x88\x97\xe5\x8f\xb7\xef\xbc\x8c\xe4\xbb\x8e1\xe5\xbc\x80\xe5\xa7\x8b\xe8\xae\xa1\xe7\xae\x97', verbose_name=b'\xe7\xac\xacN\xe5\x88\x97')),
            ],
            options={
                'verbose_name': 'Excel\u683c\u5f0f\u5b9a\u4e49',
                'verbose_name_plural': 'Excel\u683c\u5f0f\u5b9a\u4e49\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcelContraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('constraint_type', models.CharField(max_length=1, verbose_name=b'\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'R', b'\xe6\xad\xa3\xe5\x88\x99\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f'), (b'L', b'\xe5\x88\x97\xe8\xa1\xa8'), (b'C', b'COBOL\xe5\xad\x90\xe5\x8f\xa5'), (b'N', b'\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe6\x9c\x89\xe7\xa9\xba\xe6\xa0\xbc'), (b'O', b'\xe9\x9d\x9e\xe7\xa9\xba\xe5\x80\xbc'), (b'X', b'\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x80\xbc')])),
                ('regrex_formula', models.CharField(help_text=b'\xe4\xbb\x85\xe5\xbd\x93\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b\xe9\x80\x89\xe6\x8b\xa9\xe2\x80\x9c\xe6\xad\xa3\xe5\x88\x99\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f\xe2\x80\x9d\xe6\x97\xb6\xe7\x94\x9f\xe6\x95\x88', max_length=100, null=True, verbose_name=b'\xe6\xad\xa3\xe5\x88\x99\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f', blank=True)),
                ('x_from', models.CharField(help_text=b'\xe4\xbb\x85\xe5\xbd\x93\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b\xe9\x80\x89\xe6\x8b\xa9\xe2\x80\x9c\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x80\xbc\xe2\x80\x9d\xe6\x97\xb6\xe6\x9c\x89\xe6\x95\x88', max_length=100, null=True, verbose_name=b'\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x8e\x9f\xe5\x80\xbc', blank=True)),
                ('x_to', models.CharField(help_text=b'\xe4\xbb\x85\xe5\xbd\x93\xe7\xba\xa6\xe6\x9d\x9f\xe7\xb1\xbb\xe5\x9e\x8b\xe9\x80\x89\xe6\x8b\xa9\xe2\x80\x9c\xe6\x9b\xbf\xe6\x8d\xa2\xe5\x80\xbc\xe2\x80\x9d\xe6\x97\xb6\xe6\x9c\x89\xe6\x95\x88', max_length=100, null=True, verbose_name=b'\xe6\x9b\xbf\xe6\x8d\xa2\xe7\x9b\xae\xe6\xa0\x87', blank=True)),
                ('excel_col', models.ForeignKey(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe7\xba\xa6\xe6\x9d\x9f\xe7\x9a\x84\xe5\x88\x97', to='TestMIS.ExcelCol')),
            ],
            options={
                'verbose_name': 'ExcelContraint',
                'verbose_name_plural': 'ExcelContraints',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('name', models.CharField(help_text=b'D3/D4/D5...\xe7\xad\x89\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d\xe7\xa7\xb0', max_length=10, serialize=False, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d', primary_key=True)),
                ('ip', models.IPAddressField(help_text=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84IP\xe5\x9c\xb0\xe5\x9d\x80', verbose_name=b'IP\xe5\x9c\xb0\xe5\x9d\x80')),
                ('port', models.IntegerField(default=0, help_text=b'\xe4\xb8\xbb\xe6\x9c\xbaPCOM\xe7\x9a\x84IP\xe7\xab\xaf\xe5\x8f\xa3', verbose_name=b'IP\xe7\xab\xaf\xe5\x8f\xa3(\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0)')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a',
                'verbose_name_plural': '\u4e3b\u673a\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=12, verbose_name=b'\xe7\xa8\x8b\xe5\xba\x8f\xe5\x90\x8d')),
                ('pds', models.CharField(max_length=20, verbose_name=b'PDS', choices=[(b'ONL.COB.SRC', b'ONL.COB.SRC'), (b'COM.COB.SRC', b'COM.COB.SRC'), (b'BTCH.COB.SRC', b'BTCH.COB.SRC'), (b'ONL.MVSCOB.SRC', b'ONL.MVSCOB.SRC'), (b'COM.MVSCOB.SRC', b'COM.MVSCOB.SRC'), (b'BTCH.MVSCOB.SRC', b'BTCH.MVSCOB.SRC')])),
            ],
            options={
                'verbose_name': '\u7a0b\u5e8f',
                'verbose_name_plural': '\u7a0b\u5e8f\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestAnalysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program', models.ForeignKey(to='TestMIS.Program')),
            ],
            options={
                'verbose_name': '\u6d4b\u8bd5\u5206\u6790',
                'verbose_name_plural': '\u6d4b\u8bd5\u5206\u6790',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_in_program', models.CharField(max_length=100, verbose_name=b'\xe6\xa8\xa1\xe5\x9d\x97\xe5\x90\x8d')),
                ('case_no', models.CharField(max_length=8, verbose_name=b'\xe6\xa1\x88\xe4\xbe\x8b\xe5\x8f\xb7', validators=[django.core.validators.RegexValidator(regex=b'CASE\\d{4,4}')])),
                ('case_type', models.CharField(max_length=1, verbose_name=b'\xe6\xa1\x88\xe4\xbe\x8b\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'B', b'\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\x88\xe4\xbe\x8b'), (b'E', b'\xe6\x89\xa9\xe5\xb1\x95\xe6\xa1\x88\xe4\xbe\x8b')])),
                ('case_div', models.CharField(max_length=200, verbose_name=b'\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\x88\xe4\xbe\x8b\xe5\x88\x92\xe5\x88\x86', blank=True)),
                ('designer', models.CharField(max_length=15, verbose_name=b'\xe8\xae\xbe\xe8\xae\xa1\xe8\x80\x85')),
                ('case_explain', models.TextField(verbose_name=b'\xe6\xa1\x88\xe4\xbe\x8b\xe6\xb3\xa8\xe8\xa7\xa3')),
                ('case_aim', models.TextField(verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe7\x9b\xae\xe6\xa0\x87')),
                ('base_case', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x9f\xba\xe7\xa1\x80\xe6\xa1\x88\xe4\xbe\x8b\xe5\x8f\xb7', blank=True, to='TestMIS.TestCase', null=True)),
                ('test_analysis', models.ForeignKey(verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe5\x88\x86\xe6\x9e\x90', to='TestMIS.TestAnalysis')),
            ],
            options={
                'verbose_name': '\u6d4b\u8bd5\u6848\u4f8b',
                'verbose_name_plural': '\u6d4b\u8bd5\u6848\u4f8b\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point_name', models.CharField(max_length=30, verbose_name=b'\xe5\x88\x87\xe7\x89\x87\xe6\xa0\x87\xe7\xad\xbe')),
                ('point_type', models.CharField(max_length=1, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'I', '\u8f93\u5165'), (b'O', '\u8f93\u51fa')])),
                ('var_name', models.CharField(max_length=30, verbose_name=b'\xe5\x8f\x98\xe9\x87\x8f')),
                ('var_comment', models.CharField(max_length=200, verbose_name=b'\xe5\x8f\x98\xe9\x87\x8f\xe6\xb3\xa8\xe8\xa7\xa3')),
                ('var_value', models.CharField(max_length=254, verbose_name=b'\xe8\xbe\x93\xe5\x85\xa5\xe5\x80\xbc/\xe8\xa7\x82\xe6\xb5\x8b\xe5\x80\xbc')),
                ('test_case', models.ForeignKey(verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe6\xa1\x88\xe4\xbe\x8b', to='TestMIS.TestCase')),
            ],
            options={
                'verbose_name': '\u6d4b\u8bd5\u70b9',
                'verbose_name_plural': '\u6d4b\u8bd5\u70b9',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=4, verbose_name=b'\xe6\x89\xb9\xe6\xac\xa1\xe5\x8f\xb7')),
                ('alias', models.CharField(max_length=4, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe7\x8e\xaf\xe5\xa2\x83\xe5\x89\x8d\xe7\xbc\x80')),
                ('place', models.ForeignKey(verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe7\x8e\xaf\xe5\xa2\x83', to='TestMIS.Place')),
            ],
            options={
                'verbose_name': '\u6279\u6b21',
                'verbose_name_plural': '\u6279\u6b21\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testanalysis',
            name='version',
            field=models.ForeignKey(to='TestMIS.Version'),
            preserve_default=True,
        ),
    ]
