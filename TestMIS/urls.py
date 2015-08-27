from django.conf.urls import patterns, url
from TestMIS import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       # url(r'^mainframe/', views.MfListView.as_view(), name='mainframe_list'),
)
