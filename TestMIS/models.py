# -*-coding:utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator


class Place(models.Model):
    name = models.CharField(
        verbose_name='主机名',
        help_text='D3/D4/D5...等主机名称',
        max_length=10,
        primary_key=True,
    )
    ip = models.IPAddressField(
        verbose_name='IP地址',
        help_text='主机对应的IP地址',
    )
    port = models.IntegerField(
        verbose_name='IP端口(默认为0)',
        default=0,
        help_text='主机PCOM的IP端口',
    )

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = "主机列表"

    def __unicode__(self):
        return u"{0} - IP: {1}".format(self.name, self.ip)


class Program(models.Model):
    PDS_LIST = (
        'ONL.COB.SRC', 'COM.COB.SRC', 'BTCH.COB.SRC',
        'ONL.MVSCOB.SRC', 'COM.MVSCOB.SRC', 'BTCH.MVSCOB.SRC',
        )
    PDS_CHOICES = ((x, x) for x in PDS_LIST)
    name = models.CharField(
        verbose_name='程序名',
        max_length=12,
    )
    pds = models.CharField(
        verbose_name='PDS',
        max_length=20,
        choices=PDS_CHOICES,
    )

    class Meta:
        verbose_name = "程序"
        verbose_name_plural = "程序列表"

    def __unicode__(self):
        return u"{0}({1})".format(self.pds, self.name)


class Version(models.Model):

    name = models.CharField(
        verbose_name='批次号',
        max_length=4,
    )
    place = models.ForeignKey(
        verbose_name='主机环境',
        to=Place,
    )
    alias = models.CharField(
        verbose_name='主机环境前缀',
        max_length=4,
    )

    class Meta:
        verbose_name = "批次"
        verbose_name_plural = "批次列表"

    def __unicode__(self):
        return u"{0}批次: {2} on ({1})".format(self.name, self.place, self.alias)


class TestAnalysis(models.Model):

    version = models.ForeignKey(Version)
    program = models.ForeignKey(Program)

    class Meta:
        verbose_name = "测试分析"
        verbose_name_plural = "测试分析"

    def __unicode__(self):
        return u"{0} - {1}{2} ({3})".format(
            self.program.name, self.version.alias, self.program.pds,
            self.version.name,
            )


class TestCase(models.Model):
    CASE_TYPE = (
        ('B', '基础案例'),
        ('E', '扩展案例'),
    )
    (BASE_CASE, EXTEND_CASE,) = ('B', 'S',)
    test_analysis = models.ForeignKey(
        verbose_name='测试分析',
        to=TestAnalysis,
    )
    model_in_program = models.CharField(
        verbose_name='模块名',
        max_length=100
    )
    case_no = models.CharField(
        verbose_name='案例号',
        max_length=8,
        validators=[RegexValidator(regex=r'CASE\d{4,4}'), ]
    )
    case_type = models.CharField(
        verbose_name='案例类型',
        max_length=1,
        choices=CASE_TYPE,
    )
    base_case = models.ForeignKey(
        verbose_name='关联基础案例号',
        to='self',
        null=True,
        blank=True,
    )
    case_div = models.CharField(
        verbose_name='基础案例划分',
        max_length=200,
        blank=True,
    )
    designer = models.CharField('设计者', max_length=15)
    case_explain = models.TextField('案例注解')
    case_aim = models.TextField('测试目标')

    class Meta:
        verbose_name = "测试案例"
        verbose_name_plural = "测试案例列表"

    def is_base_case(self):
        return self.case_type == TestCase.BASE_CASE

    def is_extend_case(self):
        return not self.is_base_case()

    def get_readonly_fields(self):
        readonly_fileds = ['test_analysis', 'designer']
        if self.is_base_case():
            readonly_fileds.append('base_case')
        else:
            readonly_fileds.append('case_div')
        return readonly_fileds

    def query_base_cases(self):
        return TestCase.objects.filter(
            test_analysis=self.test_analysis, case_type=TestCase.BASE_CASE)

    def __unicode__(self):
        return u"{0}-{1}".format(self.test_analysis.program.name, self.case_no)


class TestPoint(models.Model):
    POINT_TYPE = (
        ('I', u'输入'),
        ('O', u'输出')
    )
    test_case = models.ForeignKey(
        verbose_name='测试案例',
        to=TestCase,
    )
    point_name = models.CharField(
        verbose_name='切片标签',
        max_length=30,
    )
    point_type = models.CharField(
        verbose_name='类型',
        max_length=1,
        choices=POINT_TYPE,
    )
    var_name = models.CharField(
        verbose_name='变量',
        max_length=30,
    )
    var_comment = models.CharField(
        verbose_name='变量注解',
        max_length=200,
    )
    var_value = models.CharField(
        verbose_name='输入值/观测值',
        max_length=254)

    class Meta:
        verbose_name = u"测试点"
        verbose_name_plural = u"测试点"

    def __unicode__(self):
        return u"{0}-TDDLBL:{1},TYPE:{2},VAR:{3}".format(
            self.test_case,
            self.point_name,
            self.point_type,
            self.var_name,
        )


class ExcelCol(models.Model):

    sheet_name = models.CharField(
        verbose_name='对应的sheet',
        max_length=21,
        help_text='excel中sheet的名字',
        default='单元测试分析',
    )

    col_name = models.CharField(
        verbose_name='列名',
        max_length=20,
        help_text='组成测试分析or案例所必要的列',
    )

    col_pos_x = models.IntegerField(
        verbose_name='第N列',
        help_text='本列在规定的excel格式要求内的列号，从1开始计算',
    )

    class Meta:
        verbose_name = "Excel格式定义"
        verbose_name_plural = "Excel格式定义列表"
        ordering = ['sheet_name', 'col_pos_x']
        # unique_together = (('sheet_name', 'col_pos_x'),)

    def __unicode__(self):
        return u"{0}'s {1} Col at {2} pos.".format(
            self.sheet_name,
            self.col_name,
            self.col_pos_x,
        )


class ExcelContraint(models.Model):

    CONSTRAINT_TYPE = (
        ('R', '正则表达式'),
        ('L', '列表'),
        ('C', 'COBOL子句'),
        ('S', '不允许有空格'),
        ('O', '非空值'),
        ('X', '替换值'),
        ('N', '允许空值'),
        ('M', '关联约束'),
    )

    (
        REGEX, LIST, CLAUSE, NON_SPACE, NOT_NULL,
        REPLACE, NULL, MULTI_CONSTRAINT,
    ) = (
        'R', 'L', 'C', 'S', 'O', 'X', 'N', 'M',
    )

    excel_col = models.ForeignKey(
        verbose_name='添加约束的列',
        to=ExcelCol,
        null=True  # 不设置这个的话，在 makemigrations TestMIS 时会提示 trying to add a non-nullable
                   # field 'excel_col' to excelcontraint without a default
    )

    constraint_type = models.CharField(
        verbose_name='约束类型',
        max_length=1,
        choices=CONSTRAINT_TYPE,
    )

    regrex_formula = models.CharField(
        verbose_name='正则表达式',
        max_length=100,
        help_text='仅当约束类型选择“正则表达式”时生效',
        null=True,
        blank=True,
    )

    x_from = models.CharField(
        verbose_name='替换原值',
        max_length=100,
        help_text='仅当约束类型选择“替换值”时有效',
        null=True,
        blank=True,
    )
    x_to = models.CharField(
        verbose_name='替换目标',
        max_length=100,
        help_text='仅当约束类型选择“替换值”时有效',
        null=True,
        blank=True,
    )
    within_list = models.CharField(
        verbose_name='枚举列表',
        max_length=200,
        validators=[RegexValidator(regex=r'(?:\S+?, ?)+'), ],
        help_text='仅当约束类型选择“列表”时有效',
        null=True,
        blank=True,
    )
    relative_from = models.ForeignKey(
        verbose_name='依赖列',
        to=ExcelCol,
        related_name='dependency col',
        null=True,
        blank=True,
    )
    relative_value = models.CharField(
        verbose_name='依赖列的取值',
        max_length=100,
        null=True,
        blank=True,
    )
    relative_constraint = models.CharField(
        verbose_name='依赖约束',
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "ExcelContraint"
        verbose_name_plural = "ExcelContraints"

    def __unicode__(self):
        return u"col {0}'s contraint: {1}".format(
            self.excel_col.col_name,
            self.constraint_type,
        )

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return self.docfile.url
