# -*-coding:utf-8 -*-
import re
import xlrd

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from TestMIS.models import ExcelContraint
from const import Const


@deconstructible
class ExcelValidator(object):
    constraints = []
    code = 'invalid'

    def __init__(self, constraints=None):
        if constraints is not None:
            self.constraints = constraints
        if not self.constraints:
            raise TypeError(
                "No constraints passed to the Validator (constraints is None)"
            )
        for c in self.constraints:
            if not isinstance(c, ExcelContraint):
                raise TypeError(
                    "Not a constraint passed to the Validator {0}".format(c)
                )
        self.errdecs = []

    def __call__(self, value):
        if self.check_constraint(value):
            raise ValidationError(self.get_first_errdesc(), code=self.code)

    @staticmethod
    def is_clause(value):
        return value.strip().find(' ') != -1

    def get_first_errdesc(self):
        if self.errdecs:
            return self.errdecs[0]
        else:
            return ''

    def check_constraint(self, value):
        for c in self.constraints:
            mode, regex, v_list = (
                c.constraint_type, c.regex_formula, c.with_list.split(','),
            )
            if mode == ExcelContraint.REGEX and re.findall(regex, value):
                self.errdecs.append(
                    Const.XL_CONSTRAINT_MSG[mode] % regex
                )
            elif mode == ExcelContraint.LIST and value in v_list:
                self.errdecs.append(
                    Const.XL_CONSTRAINT_MSG[mode] % v_list
                )
            elif mode == ExcelContraint.CLAUSE and self.is_clause(str(value)):
                self.errdecs.append(
                    Const.XL_CONSTRAINT_MSG[mode]
                )
            elif mode == ExcelContraint.NON_SPACE and value.find(' ') == -1:
                self.errdecs.append(
                    Const.XL_CONSTRAINT_MSG[mode]
                )
            elif mode == ExcelContraint.NOT_NULL\
                    and (value or value.ctype == xlrd.biffh.XL_CELL_EMPTY):
                self.errdecs.append(
                    Const.XL_CONSTRAINT_MSG[mode]
                )
        return len(self.errdecs) > 0

    def extract_value(self, cell):
        if not cell.ctype == xlrd.biffh.XL_CELL_NUMBER:
            value = cell.value
        else:
            value = str(cell.value)
            if value.endswith('.0'):
                value = value[:-2]
        for rp in self.constraints.filter(
                constraint_type=ExcelContraint.REPLACE):
            value = value.replace(rp.xfrom, rp.x_to)
        return value


class CellError(object):
    """
    存储单元格填写值的错误
    x for x coordinate, y for y coordinate,
    v for value, err_desc for error description
    """
    A_PLACE_OFFSET = 64

    def __init__(self, x, y, v, err_descs, x_to_char_flag=True):
        self.x = x
        self.y = y
        self.v = v
        self.err_descs = err_descs
        self.x_to_char_flag = x_to_char_flag

    def get_xy(self):
        return (str(self.to_char(self.x + 1)), str(self.y + 1))

    def to_char(self, x):
        if self.x_to_char_flag:
            (r, x) = divmod(x, 26)
            ch = chr(CellError.A_PLACE_OFFSET+x)
            if not r:
                return '{0}{1}'.format(
                    self.to_char(r), ch
                    )
            else:
                return ch
        else:
            return x

    def get_errdescs(self):
        return self.err_descs

    def get_value(self):
        return self.value

    def get_all(self):
        return (self.get_xy(), self.get_value(), self.get_errdescs())

    def print_err(self):
        return u'位置：{0} 值：{1} 约束：{2}'.format(
            self.get_xy, self.get_value, self.get_errdescs())
