__author__ = 'guoc'

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    # url(r'^$', views.CaseView.as_view(), name="case_results"),
    url(r'^$', views.HomeView.as_view(), name='report_home'),
    url(r'^cases/(?P<case_name>[\w\.]+)$', views.CaseView.as_view(), name="case_results"),
)
