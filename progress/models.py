from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import admin

from django.utils.timezone import now
import time

class Goal(models.Model):
    name = models.CharField(max_length=50)
    addedAt = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=10)
    targetValue = models.FloatField()
    targetDate = models.DateTimeField(null=True, blank=True)
    targetIsLess = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'addedAt'

    def save(self, *args, **kwargs):
        super(Goal, self).save(*args, **kwargs)

    def status(self):
        if len(self.update_set.all()) == 0:
            return Update(goal=self)
        return self.update_set.order_by('updatedAt').latest()

    def percentage(self):
        cur_value = self.update_set.order_by('updatedAt').latest().value

        if self.targetIsLess is True:
            cur_value = cur_value - self.targetValue
        return (cur_value / self.targetValue) * 100

    def hasTargetDate(self):
        return self.targetDate is not None

    """
    Get remaining time available
    Returns: datetime.timedelta

    """
    def remaining(self):
        if not self.hasTargetDate(): return None
        return self.targetDate - now()

    def __unicode__(self):
        return "%s: %s" % (self.name, self.status() if self.status() else '0%')

    def target(self):
        return Update(goal=self, value=self.targetValue)

class Update(models.Model):
    goal = models.ForeignKey(Goal)
    value = models.FloatField(default=0.0)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'updatedAt'

    """
    Some hard-coded formats for things like percentages

    """
    def format_unit(self, value, unit):
        formats = {'%': '%s%%'}
        if unit in formats:
            return formats[unit] % value
        return '%s %s' % (value, unit)

    def get_float_or_int(self, value):
        r = '%.2f' % value

        rem = r[r.find('.')+1:]
        if len(rem.rstrip('0')) == 0:
            return r[:r.find('.')]
        return r

    def __unicode__(self):
        val = self.get_float_or_int(self.value)
        return self.format_unit(val, self.goal.unit)

class DayLog(models.Model):
    date = models.DateField(default=now())
    summary = models.CharField(max_length=50)
    extended = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'createdAt'

    def __unicode__(self):
        return '%s: %s' % (self.date.strftime('%d/%m/%Y'), self.summary)

admin.site.register(Goal)
admin.site.register(Update)
admin.site.register(DayLog)
