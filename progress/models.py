from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import admin

class Goal(models.Model):
	name = models.CharField(max_length=50)
	addedAt = models.DateTimeField(auto_now_add=True)

	def save(self, progress=0, *args, **kwargs):
		super(Goal, self).save(*args, **kwargs)
	
		if self.pk is None:
			# Create the current status (0, if not given)
			progression = Progression(goal=self, completed=progress)
			progression.save()
	
	def status(self):
		if len(self.progression_set.all()) == 0:
			return Progression()
		return sorted(self.progression_set.all(), key=lambda k: k.updatedAt, reverse=True)[0]

	def __unicode__(self):
		return "%s: %s" % (self.name, self.status() if self.status() else '0%')

class Progression(models.Model):
	goal = models.ForeignKey(Goal)
	completed = models.FloatField(default=0.0)
	updatedAt = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "%.0f%%" % round(self.completed, 2)

admin.site.register(Goal)
admin.site.register(Progression)
