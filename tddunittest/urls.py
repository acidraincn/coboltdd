from django.conf.urls import patterns, include, url
from django.contrib import admin
# import ../admin as myadmin
from TestMIS.views import IndexView, MfListView, VerListView, ProgListView, TestAnaListView, TestCaseListView, MfDetailView, VerDetailView, ProgDetailView, TestAnaDetailView, TestCaseDetailView, upload_document
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'tddunittest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^testmis/', include('TestMIS.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', upload_document, name='upload_file'),
    url(r'^place_list/$', MfListView.as_view(), name='place_list'),
    url(r'^version_list/$', VerListView.as_view(), name='ver_list'),
    url(r'^program_list/$', ProgListView.as_view(), name='prog_list'),
    url(r'^testanalysis_list/$', TestAnaListView.as_view(), name='testana_list'),
    url(r'^testcase_list/$', TestCaseListView.as_view(), name='testcase_list'),
    url(r'^place/(?P<pk>[-_\w]+)/$', MfDetailView.as_view(), name='place_detail'),
    url(r'^version/(?P<pk>\d+)/$', VerDetailView.as_view(), name='ver_detail'),
    url(r'^program/(?P<pk>\d+)/$', ProgDetailView.as_view(), name='prog_detail'),
    url(r'^testanalysis/(?P<pk>\d+)/$', TestAnaDetailView.as_view(), name='testana_detail'),
    url(r'^testcase/(?P<pk>\d+)/$', TestCaseDetailView.as_view(), name='testcase_detail'),
) + static(settings.DOCUMENT_URL, document_root=settings.DOCUMENT_ROOT)
