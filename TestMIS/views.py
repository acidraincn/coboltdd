from django.shortcuts import render, get_object_or_404, render_to_response
from TestMIS.models import Place, Program, Version, TestAnalysis, TestCase, TestPoint, ExcelCol, ExcelContraint
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.template import RequestContext
from .forms import UploadFileForm
from .models import Document, Report
import datetime

# Create your views here.
class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'host_list'
    def get_queryset(self):
        return Place.objects.all()

class MfListView(ListView):
    model = Place
    template_name = 'place_list.html'
    # context_object_name = 'place_list'
    # def get_queryset(self):
    #     return Place.objects.all()
    # def get_context_data(self, **kwargs):
    #     context = super(ListView, self).get_context_data(**kwargs)
    #     place_list = context['object_list']
    #     return context
    # def ret_place_list(request):
    #     place_list = Place.objects.all()
    #     context = {'place_list': place_list}
    #     return render(request, 'place_list.html', context)

class MfDetailView(DetailView):
    model = Place
    template_name = 'place_detail.html'
    context_object_name = 'place_detail'
    def get_queryset(self):
        return Place.objects.all()

class VerListView(ListView):
    model = Version
    template_name = 'version_list.html'
    context_object_name = 'version_list'

class VerDetailView(DetailView):
    model = Version
    template_name = 'version_detail.html'
    context_object_name = 'version_detail'
    # def get_queryset(self):
        # return Version.objects.all()

class ProgListView(ListView):
    model = Program
    template_name = 'program_list.html'
    context_object_name = 'program_list'

class ProgDetailView(DetailView):
    model = Program
    template_name = 'program_detail.html'
    context_object_name = 'program_detail'

class TestAnaListView(ListView):
    model = TestAnalysis
    template_name = 'testanalysis_list.html'
    context_object_name = 'testanalysis_list'

class TestAnaDetailView(DetailView):
    model = TestAnalysis
    template_name = 'testanalysis_detail.html'
    context_object_name = 'testanalysis_detail'

class TestCaseListView(ListView):
    model = TestCase
    template_name = 'testcase_list.html'
    context_object_name = 'testcase_list'

class TestCaseDetailView(DetailView):
    model = TestCase
    template_name = 'testcase_detail.html'
    context_object_name = 'testcase_detail'

def upload_document(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
       ##################### begin save the .txt file to database ########################################
            f = open(newdoc.docfile.path, "r")
            for line in f.readlines():
                item = list(line.strip().split('\t'))
                prog = Program.objects.get(name=item[3])
                ta = TestAnalysis.objects.get(program=prog)
                tc = TestCase.objects.filter(test_analysis=ta, case_no=item[5])
                if len(item)==7:
                    tp = TestPoint.objects.get(test_case=tc, point_name=item[6])
                    a_status = 'B'
                    act_value = ''
                elif len(item)==11:
                    tp = TestPoint.objects.get(test_case=tc, point_name=item[6], var_name=item[8])
                    a_status = item[7]
                    act_value = item[9]
                Report.objects.create(execute_date=datetime.date(int(item[0][:4]), int(item[0][4:6]), int(item[0][6:])), execute_time=datetime.time(int(item[1][:2]), int(item[1][3:5]), int(item[1][6:])), driven_trade=item[2], test_teller=item[4], test_point=tp, status=a_status, actual_value=act_value)
       ##################### end save the .txt file to database ##########################################

            # return HttpResponse('Upload OK!')

            # Redirect to the index page after POST
            return HttpResponseRedirect(reverse(upload_document))
    else:
        form = UploadFileForm()
    documents = Document.objects.all()
    version = Version.objects.all()
    program = Program.objects.all()
    return render_to_response('upload_file.html', {'documents': documents, 'form': form, 'version': version,
                              'program': program}, context_instance=RequestContext(request)
    )
