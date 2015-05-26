from django.contrib import admin
from .models import Suite
from .models import Release
from .models import PerfCase
from .models import PerfRecord

# Register your models here.
admin.site.register(Suite)
admin.site.register(Release)
admin.site.register(PerfCase)
admin.site.register(PerfRecord)
