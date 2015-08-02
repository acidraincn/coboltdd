# -*-coding:utf-8 -*-
__all__ = ['Const', ]


class Const(object):
    """用以存储整个项目中的常量定义"""
# ------XL类常量，对读取的excel格式、约束等进行定义
# 读取的目标sheet名称
    XL_TARGET_SHEET_NAME = u'单元测试分析'
# excel的扩展名集合
    XL_FILE_EXTS = ('xls', 'xlsx', 'xlsm')
# excel标题行范围
    XL_TITLE_ROW_RANGE = [0, 1]
# 约束对应的错误信息
    XL_CONTRAINT_MSG = {
        'R': u'内容不符合正则表达式%s的定义',
        'L': u'内容不在列表范围:%s',
        'C': u'内容不为COBOL句子',
        'S': u'要求不能有空格',
        'O': u'要求非空值',
    }
    CONSTRAINT_TYPE = (
        ('R', '正则表达式'),
        ('L', '列表'),
        ('C', 'COBOL子句'),
        ('S', '不允许有空格'),
        ('O', '非空值'),
        ('X', '替换值'),
        ('N', '允许空值'),
    )
# ------XL类常量定义结束

    def __init__(self):
        pass
