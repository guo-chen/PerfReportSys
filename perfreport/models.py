import re
from django.db import models
from django.core.exceptions import ValidationError

valid_p = re.compile("^(\d{4}\.((12)|(09)|(06))(-SP\d+)?)$|dev$")


# Create your models here.
def validate_release(value):
    if not re.match(valid_p, value):
        raise ValidationError("%s is not valid. Can only have releases in\
                              format of YYYY.MM (with or without -SP2) or dev"%value)


class Suite(models.Model):
    name = models.CharField(max_length=128, help_text="The name of the suite, 128 characters allowed", unique=True)

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


class PerfCase(models.Model):
    name = models.CharField(max_length=128, help_text="The name of the case, 128 characters allowed", unique=True)
    suite = models.ForeignKey(Suite)

    def __unicode__(self):
        return self.name


class PerfRecord(models.Model):
    rel_ver = models.ForeignKey(Release)
    case = models.ForeignKey(PerfCase)
    total_mem_consumption = models.FloatField(help_text="Total Memory Consumption, in GB*Hours")
    peak_host_mem = models.FloatField(help_text="Peak Host Memory, in GB")
    overall_runtime = models.IntegerField(help_text="Overall Running Time, in seconds")
    highest_cmd_mem = models.FloatField(help_text="Highest Command Memory, in MB")
    peak_disk = models.FloatField(help_text="Peak Disk Usage, in Mb")

    def _collect_data(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        name = "_".join([self.case.suite.name, self.case.name, self.rel_ver.name])
        super(PerfRecord, self).save()

    def __unicode__(self):
        return "_".join([self.case.suite.name, self.case.name, self.rel_ver.name])
