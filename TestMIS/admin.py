# -*-coding:utf-8 -*-
from django.contrib import admin
from django.db.models import Max
from .models import Place, Program, Version, TestAnalysis, TestCase,\
                    TestPoint, ExcelContraint, ExcelCol

admin.site.register(Place)
admin.site.register(Program)
admin.site.register(Version)
admin.site.register(TestAnalysis)

# ExcelCol admin definition


class ExcelConstraintInline(admin.TabularInline):
    model = ExcelContraint
    extra = 2


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
            aggregate(Max('col_pos_x'))['col_pos_x__max']+1
        form.base_fields['col_pos_x'].initial = default_y
        return form


# TestCase admin definition


class TestPointInline(admin.TabularInline):
    model = TestPoint
    extra = 3


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    # list
    list_display = ('case_no', 'case_type', 'test_analysis')
    # detail
    radio_fields = {'case_type': admin.HORIZONTAL}
    inlines = [TestPointInline]
    fieldsets = [
        ('归属', {'fields': ['test_analysis', ]}),
        ('基本信息', {'fields': [
            'model_in_program', 'case_no', 'designer',
                    ]}),
        ('案例继承', {'fields': ['case_type', 'base_case', 'case_div']}),
        ('案例说明', {'fields': ['case_explain', 'case_aim']}),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return obj.get_readonly_fields()
        else:
            return []

    def get_form(self, request, obj=None, **kwargs):
        form = super(TestCaseAdmin, self).get_form(
                        request, obj, **kwargs)
        choices = [('', '---------'), ]
        if obj and obj.is_extend_case():
            base_cases = obj.query_base_cases()
            choices.extend((x.id, x.case_no) for x in base_cases)
            form.base_fields['base_case'].choices = choices
        return form
