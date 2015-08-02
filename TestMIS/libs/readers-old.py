# -*-coding:utf-8 -*-
__all__ = [
        'extract_and_normalize_lines',
        ]
"""EXCEL Reader Vars & Consts begeins"""
XL_TARGAET_SHEET_NAME = u'单元测试分析'
XL_TITLE_ROW_RANGE = [0,  1]
XL_MIN_COL = 12
XL_MAX_COL = 17
XL_COLS_SELECTED = (
        'case no',
        'case type',
        'div val/parent',
        'set point',
        'set var',
        'set val',
        'watch point',
        'watch var',
        'watch val',
        )
# name:(pos, type, valid_vals)
XL_ROW_FORMAT_MATRIX = {
        'case no': (( 1, ), (('r', r'CASE\d{4, 4}'), )),
        'case type': 
            ( ( 1, ),  (('l', (u'基础案例', u'特殊案例')), )), 
        'div val/parent': 
            ( ( 1, ),  (('r', r'CASE\d{4, 4}'), ('c', 'clause'))), 
        'set point': 
            ( ( 0, 1),  (('n', 'non-space'), )), 
        'set var':   
            ( ( 0, 1),  (('n', 'non-space'), )), 
        'set val':   
            ( ( 0, 1, 2), (('c', 'clause'), ('o', 'non-null'), )), 
        'watch point': 
            ( ( 0, 1),  (('n', 'non-space'), )), 
        'watch var': 
            ( ( 0, 1),  (('n', 'non-space'), )), 
        'watch val': 
            ( ( 0, 1, 2), (('c', 'clause'), ('o', 'non-null'), ))
}
#name:col-in-excel
XL_COL_COLLECT_POS = {
        'case no'           :  2, 
        'case type'         :  3, 
        'div val/parent'    :  5, 
        'set point'         :  8, 
        'set var'           :  9, 
        'set val'           : 11, 
        'watch point'       : 12, 
        'watch var'         : 13, 
        'watch val'         : 15, 
        }
#name:repalcement-tuple(orginal, target)
XL_CELL_REPLACEMENT = {
        'case type'    : ((u'基础案例', 'Y'), (u'特殊案例', 'N'), )
        }
"""""EXCEL Reader Vars & Consts ends"""
import os, xlrd, re
from cobol import Clause


class TextReader(object):
    def __init__(self, path):
        self._check_exist(path)

    def _check_exist(self, path):
        if os.path.exists(path):
            self.path = path
        elif os.path.exists('%s\\%s' % (os.getcwd(), path)):
            self.path = '%s\\%s' % (os.getcwd(), path), 'r'
        else:
            raise (ValueError, '%s not exists!' % path)

    def _open_and_read(self):
        self.f = open(self.path, 'r')
        return self.f.readlines()

    def _close(self):
        self.f.close()

    def readlines(self):
        list = self._open_and_read()
        self._close()
        return list


class ExcelReader(TextReader):
    global XL_TARGET_SHEET_NAME
    global XL_TITLE_ROW_RANGE

    def __init__(self, path):
        TextReader.__init__(self, path)
        self.path = path
        self.sheet = None
        self.start_row = 0
        self.row_bound = 0
        self._open_book_and_read_sheet()
        self._check_format()

    def _open_book_and_read_sheet(self):
        book = xlrd.open_workbook(self.path)
        if XL_TARGAET_SHEET_NAME in book._sheet_names:
            self.sheet = book.sheet_by_name(XL_TARGAET_SHEET_NAME)
            self.start_row = XL_TITLE_ROW_RANGE[-1]+1
            self.row_bound = self.sheet.nrows
            print 'sheet %s found' % self.sheet.name
        else:
            raise (ValueError, 'sheet %s not found!' % (
                    XL_TARGAET_SHEET_NAME))

    def _check_format(self):
        print 'validating excel file input: %s' % self.path
        if ConstraintValidation(self.sheet).check():
            print 'validating passed!congratulations!'
        else:
            print 'validating fails!'

    def _cell_val_with_rep(self, cell, col_name):
        if not cell.ctype == 2:
            cell_value = cell.value
        else:
            cell_value = str(cell.value)
            if cell_value.endswith('.0'):
                cell_value = cell_value[:-2]
        if col_name not in XL_CELL_REPLACEMENT.keys():
            return cell_value
        else:
            for (o, t) in XL_CELL_REPLACEMENT[col_name]:
                cell_value = cell_value.replace(o, t)
            return cell_value

    def readlines(self):
        lines = []
        for x in range(self.start_row, self.row_bound):
            row_raw = self.sheet.row(x)
            row_collected = []
            for col_name in XL_COLS_SELECTED:
                y = XL_COL_COLLECT_POS[col_name]
                cell_value = self._cell_val_with_rep(row_raw[y], col_name)
                row_collected.append(cell_value)
            lines.append('%s\n' % '\t'.join(row_collected))
        return lines


class ConstraintValidation(object):
    global XL_MIN_COL
    global XL_MAX_COL
    global XL_TITLE_ROW_RANGE

    def __init__(self, sheet):
        self.sheet = sheet
        self.st = XL_TITLE_ROW_RANGE[-1]+1
        self.rows = sheet.nrows
        self.cols = sheet.ncols

    def _check_bounds(self):
        if self.st >= self.rows:
            raise (ValueError,  'not data in the file')
        if self.cols - 1 < XL_MIN_COL or \
                self.cols - 1 > XL_MAX_COL:
            raise (
                ValueError, 'cols count out if range:\nexpect:[%s, %s]\n'
                'actual:%s' % (XL_MIN_COL, XL_MAX_COL, self.cols-1))

    def _check_cell(self, x, y, row, constraint):
        c_types, c_matches = constraint
        cell = row[y]
        if cell.ctype not in c_types:
            raise (
                ValueError, 'row %s,  col %s,  value type error!'
                % (x+1, y+1))
        val_violates = True
        for t, r in c_matches:
            if val_violates:
                if t == 'r' and re.findall(r, cell.value):
                    val_violates = False
                elif t == 'l' and cell.value in r:
                    val_violates = False
                elif t == 'c' and Clause.is_clause(str(cell.value)):
                    val_violates = False
                elif t == 'n' and cell.value.find(' ') == -1:
                    val_violates = False
                elif t == 'o' and not cell.ctype == 0:
                    val_violates = False
                else:
                    val_violates = True
        if val_violates:
            print 'rule is %s %s' % (t, r)
            print 'value %s' % cell.value
            raise (
                ValueError, 'row %s,  col %s,  value error!\n'
                % (x+1, y+1))

    def _check_row(self, row, i):
        constraint = XL_ROW_FORMAT_MATRIX['case no']
        y = XL_COL_COLLECT_POS['case no']
        self._check_cell(i, y, row, constraint)
        constraint = XL_ROW_FORMAT_MATRIX['case type']
        y = XL_COL_COLLECT_POS['case type']
        self._check_cell(i, y, row, constraint)
        constraint = XL_ROW_FORMAT_MATRIX['div val/parent']
        y = XL_COL_COLLECT_POS['div val/parent']
        self._check_cell(i, y, row, constraint)
        # set values check
        constraint = XL_ROW_FORMAT_MATRIX['set point']
        y = XL_COL_COLLECT_POS['set point']
        set_point_cell = row[y]
        if set_point_cell.value:
            self._check_cell(i, y, row, constraint)
            constraint = XL_ROW_FORMAT_MATRIX['set var']
            y = XL_COL_COLLECT_POS['set var']
            self._check_cell(i, y, row, constraint)
            constraint = XL_ROW_FORMAT_MATRIX['set val']
            y = XL_COL_COLLECT_POS['set val']
            self._check_cell(i, y, row, constraint)
        # watch values check
        constraint = XL_ROW_FORMAT_MATRIX['watch point']
        y = XL_COL_COLLECT_POS['watch point']
        watch_point_cell = row[y]
        if watch_point_cell.value:
            self._check_cell(i, y, row, constraint)
            constraint = XL_ROW_FORMAT_MATRIX['watch var']
            y = XL_COL_COLLECT_POS['watch var']
            self._check_cell(i, y, row, constraint)
            constraint = XL_ROW_FORMAT_MATRIX['watch val']
            y = XL_COL_COLLECT_POS['watch val']
            self._check_cell(i,  y,  row, constraint)

    def check(self):
        self._check_bounds()
        for i in range(self.st,  self.rows):
            self._check_row(self.sheet.row(i),  i)
        return True


def is_txt(filename):
    return filename.find('.') != -1\
            and filename[filename.rfind('.')+1:] == 'txt'


def is_excel(filename):
    return filename.find('.') != -1\
            and filename[filename.rfind('.')+1:] in ('xls',  'xlsx',  'xlsm')


def extract_and_normalize_lines(path):
    if is_txt(path):
        reader = TextReader(path)
    elif is_excel(path):
        reader = ExcelReader(path)
    else:
        reader = None
        raise (
            ValueError,
            'cannot extract the file(txt or excel only): %s' % path)
    print 'Reading file:'
    print ' %s' % os.path.abspath(path)
    return reader.readlines()


def test():
    reader = ExcelReader(u'内部测试分析-UT0772.xlsx')
    f = open('test.txt',  'w')
    for line in reader.readlines():
        f.write(line)
    f.close()

if __name__ == '__main__':
    test()
