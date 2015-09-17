# -*-coding:utf-8 -*-
from django.contrib import admin
from django.db.models import Max
from django.utils.functional import curry
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm, BaseFormSet
from .models import Place, Program, Version, TestAnalysis, TestCase,\
                    TestPoint, ExcelContraint, ExcelCol, Document, Report
from .forms import TestPointInlineFormSet, TestPointForm

admin.site.register(Place)
admin.site.register(Program)
admin.site.register(Version)
admin.site.register(TestAnalysis)

admin.site.register(Document)
admin.site.register(Report)
# admin.site.register(TestPoint)
# ExcelCol admin definition



class ExcelConstraintInline(admin.TabularInline):
    model = ExcelContraint
    extra = 2
    fk_name = "excel_col"


@admin.register(ExcelCol)
class ExcelColAdmin(admin.ModelAdmin):
    # list
    list_display = ('col_name', 'col_pos_x', 'sheet_name')
    # detail
    inlines = [ExcelConstraintInline]
    fieldsets = [
        ('列定义', {'fields': ['sheet_name', 'col_name', 'col_pos_x']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExcelColAdmin, self).get_form(
                        request, obj, **kwargs)
        default_y = ExcelCol.objects.all().\
            aggregate(Max('col_pos_x'))['col_pos_x__max'] ### + 1
        form.base_fields['col_pos_x'].initial = default_y
        return form


# TestCase admin definition

# @admin.register(TestPoint)
class TestPointInline(admin.TabularInline):
    model = TestPoint
    extra = 3
    form = TestPointForm
    formset = TestPointInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(TestPointInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        # initial = []
        #     formset = super(TestPointInline, self).get_formset(request, obj, **kwargs)
        #     formset.__init__ = curry(formset.__init__, initial=initial)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super(TestPointInline, self).get_extra(request, obj, **kwargs)
        if request.GET and request.GET.__contains__('tc_pk'):
            testcase_id = request.GET.get('tc_pk', '')
            testcase_item = TestCase.objects.get(id=testcase_id)
            extra = testcase_item.testpoint_set.count() + 3
    	# elif request.GET.__contains__('pk') == False:
    	# 	extra = 0
        return extra


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    # list
    list_display = ('case_no', 'case_type', 'test_analysis')
    # list_display_links = ('case_no', 'case_type')
    # list_editable = ['test_analysis']
    # list_filter = ('case_type',)
    # raw_id_fields = ('test_analysis',)
    save_as = True
    # view_on_site = False
    # detail
    radio_fields = {'case_type': admin.HORIZONTAL}
    my_readonly_fields = ('case_type',)
    inlines = [TestPointInline]
    fieldsets = [
        ('归属', {'fields': ['test_analysis', ]}),
        ('基本信息', {'fields': [
            'model_in_program', 'case_no', 'designer',
                    ]}),
        ('案例继承', {'fields': ['case_type', 'base_case', 'case_div']}),
        ('案例说明', {'fields': ['case_explain', 'case_aim']}),
    ]
    # readonly_fields = ('case_type',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return obj.get_readonly_fields()
        else:
            return []

    def get_form(self, request, obj=None, **kwargs):
        form = super(TestCaseAdmin, self).get_form(
                        request, obj, **kwargs)
        choices = [('', '---------'), ]
        # if request.GET.__contains__('tc_pk'):
        #     form.base_fields['test_analysis'].widget.attrs["disabled"] = True
        # elif request.GET.__contains__('base_pk'):
        # 	form.base_fields['case_type'].widget.attrs["disabled"] = "disabled"
        # 	form.base_fields['base_case'].widget.attrs["disabled"] = "disabled"
        # 	form.base_fields['test_analysis'].widget.attrs["disabled"] = "disabled"
        if obj and obj.is_extend_case():
            base_cases = obj.query_base_cases()
            choices.extend((x.id, x.case_no) for x in base_cases)
            form.base_fields['base_case'].choices = choices

        return form

    # def get_inline_instances(self, request, obj):
    #     return [inline(self.model, self.admin_site) for inline in self.inlines]
    def get_changeform_initial_data(self, request):
        if request.GET and request.GET.__contains__('tc_pk'):
            testcase_id = request.GET.get('tc_pk', '')
            testcase_item = TestCase.objects.get(id=testcase_id)
            return {
                'test_analysis': testcase_item.test_analysis,
                # 'case_no': testcase_item.case_no,
                'model_in_program': testcase_item.model_in_program,
                'case_type': testcase_item.case_type,
                'base_case': testcase_item.base_case,
                'case_div': testcase_item.case_div,
                # 'inlines': testcase_item.testpoint_set.instance
            }
        elif request.GET and request.GET.__contains__('base_pk'):
        	testcase_id = request.GET.get('base_pk', '')
        	testcase_item = TestCase.objects.get(id=testcase_id)
        	return {
        		'test_analysis': testcase_item.test_analysis,
        		'case_type': 'E',
        		'base_case': testcase_item
        	}
