from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.template import RequestContext
from .models import PerfCase, PerfRecord


# Create your views here.
class CaseView0(TemplateView):
    template_name = "perf_report.html"

    def get_context_data(self, **kwargs):
        context = super(CaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request):
        case = get_object_or_404(PerfCase, name=request.GET.get("case_name", ""))
        run_results = PerfRecord.objects.filter(case__name=case.name).order_by("-rel_ver")
        context = self.get_context_data()
        context['case'] = case
        context['run_results'] = run_results

        return render_to_response(self.template_name, context, context_instance=RequestContext(request))


class CaseView(TemplateView):
    template_name = "perf_report.html"

    def get_context_data(self, **kwargs):
        context = super(CaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, case_name):
        case = get_object_or_404(PerfCase, name=case_name)
        run_results = PerfRecord.objects.filter(case__name=case.name).order_by("-rel_ver")
        context = self.get_context_data()
        context['case'] = case
        context['run_results'] = run_results

        return render_to_response(self.template_name, context, context_instance=RequestContext(request))