from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.template import RequestContext
from .models import PerfCase, PerfRecord
import json

unit = {
    "Total Memory Consumption": "GB*Hours",
    "Peak Host Memory": "GB",
    "Overall Runtime": "Seconds",
    "Highest Command Memory": "MB",
    "Peak Disk": "MB"
}


# Create your views here.
class CaseView_old(TemplateView):
    template_name = "case.html"

    def get_context_data(self, **kwargs):
        context = super(CaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, case_name):
        case = get_object_or_404(PerfCase, name=case_name)
        run_results = PerfRecord.objects.filter(case__name=case.name).order_by("rel_ver")

        summary = {
            "Total Memory Consumption": {record.rel_ver.name: record.total_mem_consumption for record in run_results},
            "Peak Host Memory": {record.rel_ver.name: record.peak_host_mem for record in run_results},
            "Overall Runtime": {record.rel_ver.name: record.overall_runtime for record in run_results},
            "Highest Command Memory": {record.rel_ver.name: record.highest_cmd_mem for record in run_results},
            "Peak Disk": {record.rel_ver.name: record.peak_disk for record in run_results}
        }
        unit = {
            "Total Memory Consumption": "GB*Hours",
            "Peak Host Memory": "GB",
            "Overall Runtime": "Seconds",
            "Highest Command Memory": "MB",
            "Peak Disk": "MB"}

        json_data = {}
        for merit in summary:
            categories = sorted(summary[merit].keys())
            category_values = [summary[merit][k] for k in categories]
            data = {
                'title': {
                    'text': merit
                },
                'xAxis': {
                    'categories': categories
                },
                'yAxis': {
                    'title': {
                        'text': unit[merit]
                    }
                },
                'series': [{
                    'name': merit,
                    'data': category_values
                }],
                'credits': 'false',
            }
            json_data[merit] = json.dumps(data)

        context = self.get_context_data()
        context['case'] = case
        context['run_results'] = run_results
        """
        context['total_mem_consumption'] = json.dumps(total_mem_consumption)
        context['releases'] = json.dumps(total_mem_consumption.keys())
        context['tmc'] = json.dumps(total_mem_consumption.values())
        """
        context['chart_data'] = json_data

        return render_to_response(self.template_name, context, context_instance=RequestContext(request))


class CaseView(TemplateView):
    template_name = "case.html"

    def get_context_data(self, **kwargs):
        context = super(CaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, case_name):
        case = get_object_or_404(PerfCase, name=case_name)
        run_results_by_mode = {}

        for run_mode in case.run_modes.all():
            run_results = PerfRecord.objects.filter(case__name=case.name, run_mode__name=run_mode)
            summary = {
                "Total Memory Consumption": {record.rel_ver.name: record.total_mem_consumption for record in
                                             run_results},
                "Peak Host Memory": {record.rel_ver.name: record.peak_host_mem for record in run_results},
                "Overall Runtime": {record.rel_ver.name: record.overall_runtime for record in run_results},
                "Highest Command Memory": {record.rel_ver.name: record.highest_cmd_mem for record in run_results},
                "Peak Disk": {record.rel_ver.name: record.peak_disk for record in run_results}
            }
            json_data = {}
            for merit in summary:
                categories = sorted(summary[merit].keys())
                category_values = [summary[merit][k] for k in categories]
                data = {
                    'title': {
                        'text': merit
                    },
                    'xAxis': {
                        'categories': categories
                    },
                    'yAxis': {
                        'title': {
                            'text': unit[merit]
                        }
                    },
                    'series': [{
                        'name': merit,
                        'data': category_values
                    }],
                    'credits': 'false',
                }
                json_data[merit] = json.dumps(data)
            run_results_by_mode[run_mode] = json_data

        context = self.get_context_data()
        context['case'] = case
        context['run_results_by_mode'] = run_results_by_mode

        return render_to_response(self.template_name, context, context_instance=RequestContext(request))
