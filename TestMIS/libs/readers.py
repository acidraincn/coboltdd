# -*-coding:utf-8 -*-
import xlrd

from const import Const
from validators import ExcelValidator, CellError
from TestMIS.models import ExcelContraint, ExcelCol


class ExcelReader(object):
    """ExcelReader
       excel 文档阅读器，如以下文档类别:
        *.xls, *.xlsx, *.xlsm
    """

    def __init__(self, p):
        self.path = p
        self.book = None
        self.sheet = None
        self.start_row = 0
        self.row_bound = 0
        self.selected_lines = []

    def _open_book_and_read_sheet(self):
        '''
        read the percific sheet pre-define by Const Var
        '''
        self.book = xlrd.open_workbook(self.path)
        if Const.XL_TARGET_SHEET_NAME in self.book._sheet_names:
            self.sheet = self.book.sheet_by_name(Const.XL_TARGET_SHEET_NAME)
            self.start_row = Const.XL_TITLE_ROW_RANGE[-1]+1
            self.row_bound = self.sheet.nrows
        else:
            raise (
                ValueError,
                'sheet %s not found in document' % Const.XL_TARGET_SHEET_NAME)

    def _select_lines(self):
        if not self.sheet:
            self._open_book_and_read_sheet()
        for y in range(self.start_row, self.row_bound):
            cols_dict, cell_errs = ({}, [])
            for col in ExcelCol.objects.filter(
                    sheet_name=Const.XL_TARGET_SHEET_NAME):
                x = col.col_pos_x - 1
                constraints = ExcelContraint.objects.filter(excel_col=col)
                cell = self.sheet.row(y)[x]
                validator = ExcelValidator(constraints)
                value = validator.extract_value(cell)
                if validator.check_constraint(value):
                    cell_errs.append([
                        CellError(x, y, value, e)
                        for e in validator.get_errdescs
                    ])
                cols_dict[col.col_name] = value
            cols_dict['errs'] = cell_errs
            self.selected_lines.append(cols_dict)
            yield cols_dict

    def readlines(self):
        '''
        按预定义的列，将单元测试分析的内容读取出来
        目前选取的列有：
            程序  模块编号    案例号 案例类型
            分析人 基础案例划分或关联的基础案例  功能描述    测试目的
            设值点 输入字段    字段描述    设值
            观测点 输出字段    字段描述    预期值
        '''
        if not self.selected_lines:
            return self._select_lines()
        else:
            return self.selected_lines
