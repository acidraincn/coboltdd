#-*-coding:utf-8 -*-
HEADER_PATH = './templates/TEMPLATE_HEADER.CBL'
FOOTER_PATH = './templates/TEMPLATE_FOOTER.CBL'

CURR_CASE        = ""
CURR_TEST_POINT  = ""
CURR_CASE_LABEL  = ""
CREATE_FUNC      = ""

from writers import FileWriter
import re,os

class Line(object):
    """
    按COBOL编辑区格式化输出行，包含标签(label)、行类型(line_type)、缩进
    (ofst)和正文(stm)设置
    """
    global CREATE_FUNC
    MAX_STM_LEN     = 65
    BASE_OFFSET     = 0
    COL_4_FIX_VERB  = 44
    VERBS_2_FIX = ('TO','USING','FROM')
    VERBS_MUST_FIX  = ('USING',)
    def __init__(self,lbl,line_type,stm,ofst):
        self.l = lbl
        self.t = line_type
        self.s = stm
        self.o = Line.BASE_OFFSET + ofst

    def get_label(self):
        return self.l
    def get_line_type(self):
        return self.t
    def get_offset(self):
        return self.o
    def get_statement(self):
        return self.s
    @staticmethod
    def line_format(l,t,s,o):
        """
        l lable_str,t line_type_str,s statement_str,o offset_int
        format cobol line(s) output
        """
        #增加缩进
        stm_str = '%s%s' % (' ' * o,s)
        #固定列
        for v in Line.VERBS_2_FIX:
            if stm_str.find(v) != -1:
                stm_str = Line.fix_to_col(stm_str,v)
            else:
                pass

        if len(stm_str) <= Line.MAX_STM_LEN:
            #正常返回
            return '%s%s%s\n' % (l,t,stm_str)
        else:
            #超长截断换行
            if stm_str.endswith('"'):
                #字符串引号结尾换行
                left_side = '%s%s%s"\n' % \
                        (l,t,stm_str[:Line.MAX_STM_LEN-1])

                right_side = '%s%s' % \
                        ('"',stm_str[Line.MAX_STM_LEN-1:])
                left_qoute_p = stm_str.find('"')
                right_side = Line.line_format(
                        l,t,right_side,left_qoute_p-1)
                return '%s%s' % (left_side,right_side)
            else:
                #对固定位置列进行折行
                for v in Line.VERBS_2_FIX:
                    if v not in Line.VERBS_MUST_FIX:
                        v_p = stm_str.find(' %s ' % v)
                        if v_p != -1:
                            left = Line.line_format(
                                    l,t,stm_str[:v_p].rstrip(),0)
                            right = '%s%s%s\n' % (
                                    l,t,
                                    Line.algin_to_right(stm_str[v_p+1:])
                                    )
                            return '%s%s' % (left,right)
                #从右往左按词折行
                sp_p = stm_str.strip().rfind(' ')
                if sp_p != -1:
                    sp_p = stm_str.rstrip().rfind(' ')
                    ro = stm_str.rfind(' ',0,sp_p)
                    if ro == -1:
                        ro = o
                    else:
                        ro += 1
                    left_side = stm_str[:sp_p].strip()
                    right_side = stm_str[sp_p:].strip()
                    return '%s%s' %(
                            Line.line_format(l,t,left_side,o),
                            Line.line_format(l,t,right_side,ro)
                            )
                else:
                    #按最大值折行
                    offset = len(stm_str) - Line.MAX_STM_LEN + 1
                    return '%s%s%s\n' % (l,t,stm_str[offset:])
    @staticmethod
    def algin_to_right(s):
        s = s.strip()
        offset = Line.MAX_STM_LEN - len(s)
        return '%s%s' % (' ' * offset,s)
    @staticmethod
    def fix_to_col(s,v):
        """
        s str.
        Put TO Verb in the fixed column
        """
        fix = Line.COL_4_FIX_VERB - len(v)
        max = Line.MAX_STM_LEN
        rt  = s
        old_p = s.find(' %s ' % v)
        left = s[:old_p].rstrip()
        right = s[old_p:].lstrip()
        if old_p == -1:
            return rt
        else:
            old_p += 1
            if old_p < fix:
                offset = fix - old_p
                rt = '%s%s%s' % (s[:old_p],' ' * offset, s[old_p:])
            elif old_p > fix:
                offset = max - len(s) + 1
                rt = '%s%s%s' % (' ' * offset,s[:old_p],s[old_p:])
            if len(rt) > max and v not in Line.VERBS_MUST_FIX:
                min_len = len(left) + len(right)
                if min_len + 1 <= max:
                    rt = '%s%s%s' % (left,' ',right)
        return rt

    def __str__(self):
        return self.to_str()
    def to_str(self):
        return Line.line_format(self.l,self.t,self.s,self.o)

class Statement(object):
    STM_OFFSET     = 4
    BASE_INDENT    = 3
    DYNAMIC_OFFSET = 0
    def __init__(self,label,words):
        self.l = label
        self.t = line_type = ' '
        if isinstance(words,list):
            self.ws = words
        elif isinstance(words,tuple):
            self.ws = list(words)
        elif isinstance(words,str):
            self.ws = []
            self.appendword(words)
        self.o = Statement.STM_OFFSET + Statement.BASE_INDENT
    def append_word(self,word):
        self.ws.append(word)
    def get_first_word(self):
        if len(self.ws):
            return self.ws[0]
        else:
            return None
    def __str__(self):
        return self.to_str()
    def to_str(self):
        stm_str =  ' '.join([ w.to_str() for w in self.ws])

        vn = self.get_first_word().to_str()

        indents = Statement.DYNAMIC_OFFSET
        indents = Indent.backspace(vn,indents)

        self.o += indents

        line = Line(self.l,self.t,stm_str,self.o)

        indents = Indent.indent(vn,indents)
        Statement.DYNAMIC_OFFSET = indents

        return line.to_str()

class Indent(object):
    I_DICT = {
            'IF':(False,3),
            'ELSE':(True,3),
            'END-IF':(True,0),
            'EVALUATE':(False,1),
            'WHEN':(True,2),
            'END-EVALUATE':(True,0)
            }
    I_LIST = []
    LAST_INDENT = None
    @staticmethod
    def _first_when(v):
        return v == 'WHEN' and Indent.LAST_INDENT == 'EVALUATE'
    @staticmethod
    def _should_back(v):
        return Indent.I_DICT[v][0]
    @staticmethod
    def backspace(v,l_o):
        r = l_o
        d = Indent.I_DICT
        if v in d.keys():
            if Indent._should_back(v):
                if Indent._first_when(v):
                    r = l_o
                elif len(Indent.I_LIST) > 0:
                    r =  Indent.I_LIST.pop()
                    if v =='END-EVALUATE' and len(Indent.I_LIST)>0: 
                        r = Indent.I_LIST.pop()
                else:
                    r = l_o
        elif Indent.LAST_INDENT == 'WHEN' and r == l_o:
            r = l_o + d['WHEN'][1]
        return r

    @staticmethod
    def _continous_when(v):
        return v == 'WHEN' and Indent.LAST_INDENT == 'WHEN'
    @staticmethod
    def indent(v,l_o):
        r = 0
        d = Indent.I_DICT
        if v in d.keys():
            if not Indent._continous_when(v):
                r = d[v][1]
            else:
                r = 0
            Indent.LAST_INDENT = v
            if d[v][1] > 0:
                Indent.I_LIST.append(l_o)
        return r + l_o


class Var(object):
    def __init__(self,var):
        self.v = var.strip()
        l = len(self.v)
        if l <= 30:
            pass
        else:
            raise TypeError,'Var name too long, %s : %s' % (self.v,l)
    def __str__(self):
        return self.to_str()
    def to_str(self):
        return self.v
class Clause(object):
    def __init__(self,c):
        self.c = c.strip()

    @staticmethod
    def is_clause(c):
        return c.strip().find(' ') <> -1

    def __str__(self):
        return self.to_str()
    def to_str(self):
        return self.c
class Verb(object):
    avaliable_verbs = (
            'IF','ELSE','END-IF','EVALUATE','WHEN','OTHER','END-EVALUATE',
            'MOVE','TO','ADD','SUBTRACT','FROM','COMPUTE','=','NOT','>',
            '<','>=','<=','TRUE','FALSE','CALL','USING'
            )
    def __init__(self,v):
        self.v = v.strip().upper()
        if self.v in Verb.avaliable_verbs:
            pass
        else:
            raise TypeError,'verb %s not allowed' % self.v

    def __str__(self):
        return self.to_str()
    def to_str(self):
        return self.v
class Value(object):
    TABOOES = [
            'ZERO','ZEROES','SPACE','SPACES',
            ]
    def __init__(self,w,supress=False):
        self.w = w.strip()
        self.s = supress

    @staticmethod
    def is_num(w):
        return len(re.findall(r'^\-{0,1}[\d,]+(?:\.\d+){0,1}$',\
                w.strip())) == 1
    @staticmethod
    def eliminate_qoute(w):
        if w.startswith('"'):
            w = w[1:]
        if w.endswith('"'):
            w = w[:-1]
        return w
    @staticmethod
    def add_qoute(w):
        if not w.startswith('"'):
            w = '"%s' % w
        if not w.endswith('"'):
            w = '%s"' % w
        return w
    @staticmethod
    def eliminate_comma(w):
        return w.replace(',','')
    def print_val(self):
        if self.is_num(self.w):
            return self.w
        elif self.w == "" or self.w == '""':
            return 'SPACES'
        else:
            return self.eliminate_qoute(self.w)

    def literal_val(self):
        if Clause.is_clause(self.w):
            return Clause(self.w).to_str()
        elif self.is_num(self.w) and not self.s:
            return self.eliminate_comma(self.w)
        elif self.is_num(self.w) and self.s:
            return self.add_qoute(self.eliminate_comma(self.w))
        elif self.w == "" or self.w == '""':
            return 'SPACES'
        elif self.w in Value.TABOOES:
            return self.w
        else:
            return self.add_qoute(self.w)
    def __str__(self):
        return self.to_str()
    def to_str(self):
        return self.literal_val()
#cobol wrappers starts
def make_comment(c):
    return Line(lbl=' '*6,line_type='*',stm=c,ofst=0).to_str()
def make_clause(c):
    words = [Clause(c),]
    return Statement(CURR_CASE_LABEL,words).to_str()
def make_cobol(label,words):
    return Statement(label,words).to_str()
def make_evaluate_caseno():
    return make_evaluate('TEST-CASE-NO')
def make_evaluate(v):
    words = [Verb('EVALUATE'),Var(v)]
    return make_cobol(' ' * 6,words)
def make_when(val):
    words = [Verb('WHEN'),Value(val)]
    return make_cobol(CURR_CASE_LABEL,words)
def make_evaluate_end():
    words = [Verb('END-EVALUATE'),]
    return make_cobol(' ' * 6,words)
def make_if_testpoint(p):
    words = [Var('TEST-POINT'),Clause(' = '),Value(p)]
    return make_if(words)
def make_if(words):
    ws = [Verb('IF'),]
    ws.extend(words)
    return make_cobol(CURR_CASE_LABEL,ws)
def make_else():
    ws = [Verb('ELSE'),]
    return make_cobol(CURR_CASE_LABEL,ws)
def make_end_if():
    words = [Verb('END-IF'),]
    return make_cobol(CURR_CASE_LABEL,words)
def make_move(f,t):
    words = [Verb('MOVE'),f,
            Verb('TO'),Var(t)]
    return make_cobol(CURR_CASE_LABEL,words)
def make_add(s,t):
    words = [Verb('ADD'),s,Verb('TO'),t]
    return make_cobol(CURR_CASE_LABEL,words)
def make_call(pgm,using):
    words = [Verb('CALL'),pgm,Verb('USING')]
    words.extend(using)
    return make_cobol(CURR_CASE_LABEL,words)
#cobol wrappers ends

def watch_a_val(n,v):
    """
    n name_str, v value_str
    a name,value pair will construct cobol source code like this ^_^
---------------------------------------------------------------------------
CS9999            IF TEST-POINT = "AF-INT-ACCR-B4-TRAN"
CS9999               MOVE TEST-POINT            TO DWTDD-TEST-POINT-MSG
CS9999               MOVE "WA-INT-B4-CAPN-COMP" TO DWTDD-OUTPUT-VAR-MSG
CS9999               MOVE "100.00000"           TO DWTDD-REQUIRED-VALUE
CS9999               MOVE WA-INT-B4-CAPN-COMP   TO WK-TEMP-14-DOT
CS9999               MOVE WK-TEMP-TXT-14-DOT   TO DWTDD-ACTUAL-LEFT
CS9999               MOVE WA-INT-B4-CAPN-COMP   TO WK-TEMP-2-6
CS9999               MOVE WK-TEMP-TXT-6        TO DWTDD-ACTUAL-RIGHT
CS9999               IF WA-INT-B4-CAPN-COMP NOT = 100.00000
CS9999                  MOVE "N"                TO DWTDD-EQUAL-FLAG
CS9999               ELSE
CS9999                  MOVE "Y"                TO DWTDD-EQUAL-FLAG
CS9999                  ADD 1                   TO WK-CASE-SUCC-AMT
CS9999               END-IF
CS9999               CALL "DWTDD"            USING DWTDD-COM-AREA
CS9999                                             DWTDD-RPT-COM-AREA
CS9999            END-IF
---------------------------------------------------------------------------
    """
    val_codes = []
    val_codes.append(make_move(
        Value(n),'DWTDD-OUTPUT-VAR-MSG'))
    val_codes.append(make_move(
        Value(v,supress=True),'DWTDD-REQUIRED-VALUE'))
    val_codes.append(make_move(
        Clause('SPACES'),'DWTDD-ACTUAL-VALUE'))
    if Value.is_num(v):
        val_codes.append(make_move(
            Var(n),'WK-TEMP-14-DOT'))
        val_codes.append(make_move(
            Var('WK-TEMP-TXT-14-DOT'),'DWTDD-ACTUAL-LEFT'))
        val_codes.append(make_move(
            Var(n),'WK-TEMP-2-6'))
        val_codes.append(make_move(
            Var('WK-TEMP-TXT-6'),'DWTDD-ACTUAL-RIGHT'))
    else:
        val_codes.append(make_move(
            Var(n),'DWTDD-ACTUAL-VALUE'))
    words = [Var(n),Clause('NOT ='),Value(v)]
    val_codes.append(make_if(words))
    val_codes.append(make_move(
        Value('N'),'DWTDD-EQUAL-FLAG'))
    val_codes.append(make_else())
    val_codes.append(make_move(
        Value('Y'),'DWTDD-EQUAL-FLAG'))
    val_codes.append(make_add(Value('1'),Var('WK-CASE-SUCC-AMT')))
    val_codes.append(make_end_if())
    val_codes.append(make_call(Value('DWTDD'),[
            Var('DWTDD-COM-AREA'),Var('DWTDD-RPT-COM-AREA')]))
    return val_codes


def watch_vals(case_dict,reverse=False):
    global CURR_CASE,CURR_CASE_LABEL,CURR_TEST_POINT
    case_keys = case_dict.keys()
    case_keys.sort()
    if reverse:
        case_keys.reverse()
    watch_codes = []
    watch_codes.append(make_comment('WATCH STARTS...'))
    watch_codes.append(make_evaluate_caseno())
    for case_no in case_keys:
        case = case_dict[case_no]
        CURR_CASE = case_no
        CURR_CASE_LABEL = case.get_case_label()
        CURR_TEST_POINT = None
        watch_codes.append(make_when(case_no))
        for p,n,v in case.get_watch_vals():
            if CURR_TEST_POINT != p:
                if CURR_TEST_POINT:
                    watch_codes.append(make_end_if())
                CURR_TEST_POINT = p
                watch_codes.append(\
                        make_if_testpoint(CURR_TEST_POINT))
                #watch_codes.extend(make_move(\
                        #Var('TEST-POINT'),'DWTDD-TEST-POINT-MSG'))
            watch_codes.extend(
                    watch_a_val(n,v))
        watch_codes.append(make_end_if())
    watch_codes.append(make_evaluate_end())
    watch_codes.append(make_comment('WATCH ENDS...'))
    return watch_codes

def set_div(base_dict):
    global CURR_CASE,CURR_CASE_LABEL
    CURR_CASE = None
    CURR_CASE_LABEL = None
    case_keys = base_dict.keys()
    case_keys.sort()
    case_keys.reverse()
    div_codes = []
    div_codes.append(make_comment('DIV STARTS...'))
    div_codes.append(make_evaluate_caseno())
    for case_no in case_keys:
        case = base_dict[case_no]
        CURR_CASE = case_no
        CURR_CASE_LABEL = case.get_case_label()
        div_codes.append(make_when(case_no))
        for child_case_no in case.get_children():
            div_codes.append(make_when(child_case_no))
        div_codes.append(make_move(
            Value(case.get_div_val()),case.get_div_var_name()))
    CURR_CASE_LABEL = None
    div_codes.append(make_evaluate_end())
    div_codes.append(make_comment('DIV ENDS...'))
    return div_codes

def set_vals(case_dict,case_type,reverse=False):
    global CURR_CASE,CURR_CASE_LABEL,CURR_TEST_POINT
    CURR_CASE = None
    CURR_CASE_LABEL = None
    CURR_TEST_POINT = None
    case_keys = case_dict.keys()
    case_keys.sort()
    if reverse:
        case_keys.reverse()
    set_codes = []
    set_codes.append(make_comment('%s SET STARTS...' % case_type.upper()))
    for case_no in case_keys:
        case = case_dict[case_no]
        if not CURR_CASE:
            if case_type == 'special':
                set_codes.append(make_evaluate_caseno())
            else:
                set_codes.append(make_evaluate(case.get_div_var_name()))
        CURR_CASE = case_no
        CURR_CASE_LABEL = case.get_case_label()
        if case_type == 'special':
            set_codes.append(make_when(case_no))
        else:
            set_codes.append(make_when(case.get_div_val()))
        CURR_TEST_POINT = None
        for p,n,v in case.get_set_vals():
            if CURR_TEST_POINT != p:
                if CURR_TEST_POINT:
                    set_codes.append(make_end_if())
                CURR_TEST_POINT = p
                set_codes.append(make_if_testpoint(CURR_TEST_POINT))
            if not Clause.is_clause(v):
                set_codes.append(make_move(Value(v),n))
            else:
                set_codes.append(make_clause(v))
        set_codes.append(make_end_if())
    set_codes.append(make_evaluate_end())
    set_codes.append(make_comment('%s SET ENDS...' % case_type.upper()))
    return set_codes

def output_header(output,func,pgm_name):
    if func == 'all':
        header = open(HEADER_PATH,'r').read()
        twriter = FileWriter(output)
        twriter.write(header % pgm_name)
        twriter.close()
        print "%s's header written" % pgm_name
    else:
        print "%s's header not written cause func incr"

def output_watch_vals(output,base_dict,special_dict,pgm_name):
    twriter = FileWriter(output)
    twriter.append(''.join(watch_vals(base_dict,reverse=True)))
    twriter.append(''.join(watch_vals(special_dict)))
    twriter.close()
    print "%s's watch point written" % pgm_name

def output_div(output,base_dict,pgm_name):
    twriter = FileWriter(output)
    twriter.append(''.join(set_div(base_dict)))
    twriter.close()
    print "%s's base case devide written" % pgm_name

def output_set_vals(output,base_dict,special_dict,pgm_name):
    twriter = FileWriter(output)
    twriter.append(''.join(set_vals(base_dict,'base',reverse=True)))
    twriter.append(''.join(set_vals(special_dict,'special')))
    twriter.close()
    print "%s's set point written" % pgm_name

def output_footer(func,output,pgm_name):
    if func == 'all':
        footer = open(FOOTER_PATH,'r').read()
        twriter = FileWriter(output)
        twriter.append(footer)
        twriter.close()
        print "%s's footer written" % pgm_name
    else:
        print "%s's footer not written cause func incr"  % pgm_name

def construct_cobol_src(output,base_dict,special_dict,func,pgm_name):
    global CREATE_FUNC
    CREATE_FUNC = func
    output_header(output,func,pgm_name)
    output_watch_vals(output,base_dict,special_dict,pgm_name)
    output_div(output,base_dict,pgm_name)
    output_set_vals(output,base_dict,special_dict,pgm_name)
    output_footer(func,output,pgm_name)
    print 'COBOL source file created, plz check:'
    print ' %s' % os.path.abspath(output)
