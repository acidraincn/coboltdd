from django.shortcuts import render, get_object_or_404, render_to_response
from TestMIS.models import Place, Program, Version, TestAnalysis, TestCase, TestPoint, ExcelCol, ExcelContraint
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.template import RequestContext
from .forms import UploadFileForm
from .models import Document

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
