from django.contrib import admin
from .models import Site
from .models import Suite
from .models import Release
from .models import RunMode
from .models import PerfCase
from .models import PerfRecord


class PerfCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'suite', 'site', )
    search_fields = ('name', )
    list_filter = ('suite', 'site', )


class PerfRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'rel_ver', 'run_mode')
    search_fields = ('name', )
    list_filter = ('rel_ver', )

# Register your models here.
admin.site.register(Site)
admin.site.register(Suite)
admin.site.register(Release)
admin.site.register(RunMode)
admin.site.register(PerfCase, PerfCaseAdmin)
admin.site.register(PerfRecord, PerfRecordAdmin)
