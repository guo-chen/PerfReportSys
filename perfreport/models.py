import re
from django.db import models
from django.core.exceptions import ValidationError

valid_p = re.compile("^(\d{4}\.((12)|(09)|(06))(-SP\d+)?)$|dev$")
valid_runmode = re.compile("^DP\d\d?((TH\d\d?)|(TL))$")


# Create your models here.
def validate_release(value):
    if not re.match(valid_p, value):
        raise ValidationError("%s is not valid. Can only have releases in\
                              format of YYYY.MM (with or without -SP2) or dev" % value)


def validate_runmode(value):
    if not re.match(valid_runmode, value):
        raise ValidationError("%s is not valid. Can only have run_mode in format of DPxxTHxx or DPxxTL" % value)


class Suite(models.Model):
    name = models.CharField(max_length=128, help_text="The name of the suite, 128 characters allowed", unique=True)

    def __unicode__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=128,
                            help_text="The name of site, 128 characters allowed",
                            default="MTV",
                            unique=True)

    def __unicode__(self):
        return self.name


class Release(models.Model):
    name = models.CharField(max_length=11,
                            validators=[validate_release],
                            help_text="Releases in format of YYYY.MM (with or without -SPn) or dev, default is dev",
                            default="dev",
                            unique=True)

    def __unicode__(self):
        return self.name


class RunMode(models.Model):
    name = models.CharField(max_length=8,
                            validators=[validate_runmode],
                            help_text="Running mode in format of DPxxTHxx or DPxxTL",
                            unique=True)

    def __unicode__(self):
        return self.name


class PerfCase(models.Model):
    LIBRARY_CHOICES = (
        ('GDSII', 'gds'),
        ('OASIS', 'oas'),
        ('OPENACCESS', 'oa'),
        ('MILKYWAY', 'mw'),
    )
    name = models.CharField(max_length=128, help_text="The name of the case, 128 characters allowed")
    suite = models.ForeignKey(Suite)
    site = models.ForeignKey(Site)
    run_modes = models.ManyToManyField(RunMode, blank=True)
    owner = models.CharField(max_length=64, default="", help_text="Name of the case owner who added this case")
    owner_email = models.EmailField(blank=True, help_text="Email of the owner")
    case_location = models.CharField(max_length=256, default="", help_text="Location of the case")
    result_location = models.CharField(max_length=256, default="", help_text="Location of run results of the case")
    input_library_name = models.CharField(max_length=256, default="", help_text="Input library name")
    input_library_type = models.CharField(max_length=16, choices=LIBRARY_CHOICES, default="", help_text="Input library type")
    input_library_size = models.CharField(max_length=256, default="", help_text="Input library size")
    top_cell_name = models.CharField(max_length=256, default="", help_text="Top cell name")
    number_of_commands = models.IntegerField(default=0, help_text="Total number of commands")
    number_of_commands_with_errors = models.IntegerField(default=0, help_text="The number of commands with errors")
    total_errors = models.IntegerField(default=0, help_text="Total number of errors (may vary between different flows, default is DRC flow")
    DBU = models.FloatField(default=0.0, help_text="DBU used for the database resolution")
    number_of_unique_cells_with_errors = models.IntegerField(default=0, help_text="Total number of unique cells with errors")

    class Meta:
        unique_together = ('name', 'suite', 'site',)

    def __unicode__(self):
        return self.name


class PerfRecord(models.Model):
    rel_ver = models.ForeignKey(Release)
    case = models.ForeignKey(PerfCase)
    run_mode = models.ForeignKey(RunMode)
    total_mem_consumption = models.FloatField(help_text="Total Memory Consumption, in GB*Hours")
    peak_host_mem = models.FloatField(help_text="Peak Host Memory, in GB")
    overall_runtime = models.IntegerField(help_text="Overall Running Time, in seconds")
    highest_cmd_mem = models.FloatField(help_text="Highest Command Memory, in MB")
    peak_disk = models.FloatField(help_text="Peak Disk Usage, in MB")
    name = models.CharField(max_length=256, blank=True, editable=False)

    class Meta:
        unique_together = ('case', 'rel_ver', 'run_mode',)

    def _collect_data(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = "_".join([self.case.site.name,
                              self.case.suite.name,
                              self.case.name,
                              self.rel_ver.name,
                              self.run_mode.name])
        super(PerfRecord, self).save()

    def __unicode__(self):
        return self.name
