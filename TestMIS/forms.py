# coding: utf-8

from django import forms
from django.forms.models import BaseInlineFormSet, ModelForm
from django.forms.formsets import BaseFormSet, formset_factory
from .models import TestCase, TestPoint, Version, Program
from django.forms import ModelChoiceField


class TestCaseForm(ModelForm):

    class Meta:
        model = TestCase
        fields = '__all__'


class TestPointForm(ModelForm):

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)

    class Meta:
        model = TestPoint
        fields = '__all__'


class TestPointInlineFormSet(BaseInlineFormSet):
    model = TestPoint

    def __init__(self, *args, **kwargs):
        # super(TestPointInlineFormSet, self).__init__(*args, **kwargs)
        # BaseFormSet._construct_form(self)
        if self.request.GET and self.request.GET.__contains__('tc_pk'):
            testcase_id = self.request.GET.get('tc_pk', '')
            testcase_item = TestCase.objects.get(id=testcase_id)
            tc = testcase_item.testpoint_set.all()

            initial = []
            for tp in tc:
                initial.append(
                    {'point_name': tp.point_name, 'point_type': tp.point_type, 'var_name': tp.var_name,\
                     'var_comment': tp.var_comment, 'var_value': tp.var_value},
                    # {'point_type': tc.point_type},
                    # {'var_name': tc.var_name},
                    # {'var_comment': tc.var_comment},
                    # {'var_value': tc.var_value}
                )
            print initial
            kwargs['initial'] = initial

        super(TestPointInlineFormSet, self).__init__(*args, **kwargs)

class UploadFileForm(forms.Form):
    # filename = forms.CharField(max_length=100)
    # version = forms.ChoiceField()
    # program = forms.ChoiceField()
    version = ModelChoiceField(queryset=Version.objects.all(), empty_label="请选择批次")
    program = ModelChoiceField(queryset=Program.objects.all(), empty_label="请选择程序")
    docfile = forms.FileField(label='Select a file')
