from django import forms
from .models import TestCase, TestPoint


class TestCaseForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = '__all__'


class TestPointForm(forms.ModelForm):

    class Meta:
        model = TestPoint
        fields = '__all__'
