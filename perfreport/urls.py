__author__ = 'guoc'

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    #url(r'^$', views.CaseView.as_view(), name="case_results"),
    url(r'^(?P<case_name>[\w\.]+)$', views.CaseView.as_view(), name="case_results"),
)
