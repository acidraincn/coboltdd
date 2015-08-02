# -*-coding:utf-8 -*-

from TestMIS.models import TestCase, TestPoint, ExcelCol
from TestMIS.libs.const import Const


class TestCaseWriter(TestCase):
    def __init__(self):
        super(TestCaseWriter, self).__init__()
        self.excel_dict_lines = None

    @staticmethod
    def _rasie_type_error(v, t):
        raise TypeError("{0} required for {1}, but {2}".format(t, v, type(v),))

    def _check_excel_dict_lines_types(self):
        v = self.excel_dict_lines
        if not (isinstance(v, list) or isinstance(v, tuple)):
            TestCaseWriter._rasie_type_error(v, list)
        if len(v):
            first_line = v[0]
            if not isinstance(first_line, dict):
                TestCaseWriter._rasie_type_error(first_line, dict)
            for col in ExcelCol.objects.filter(
                    sheet_name=Const.XL_TARGET_SHEET_NAME):
                if col.col_name not in first_line.keys():
                    raise ValueError(
                        "col {0} required in line_dict".format(col.col_name)
                    )
            if 'errs' not in first_line.keys():
                raise ValueError("errors description required in line_dict")

    def write_from_excel_reader_dict_lines(self, excel_dict_lines):
        self.excel_dict_lines = excel_dict_lines
        self._check_excel_dict_lines_types()
