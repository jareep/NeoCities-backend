from django.db import models

# Create your models here.

class Scenario(models.Model):
	events = models.ManyToManyField(Event)
	roles = models.ManyToManyField(Role)


class Event(models.Model):
	success_resources = models.ManyToManyField(Resource, through='Threshold')
	icon = models.FileField(upload_to='icons/events/')
	star_time = models.DateTimeField()
	description = models.TextField()
	details = models.TextField()


class Threshold(models.Model):
	order = models.IntegerField()
	amount = models.IntegerField()
	enforce_order = models.BooleanField(default=False)


class Role(models.Model):
	name = models.TextField()
	icon = models.FileField(upload_to='icons/roles/')
	resources = models.ManyToManyField(Resource, through='ResourceDepot')

class ResourceDepot():
	quantity = models.IntegerField()
	role = models.ForeignKey(Role)
	resource = models.ForeignKey(Resource)

class Resource(models.Model):
	name = models.TextField()
	icon = models.FileField(upload_to='icons/')


class Briefing(models.Model):
	details = models.TextField()
	role = models.ForeignKey(Role)
	scenario = models.ForeignKey(Scenario)


# Logging Info


class Session(models.Model):
	scenario_ran = models.ForeignKey()
	session_token = models.TextField()
	participants = models.ForeignKey()
	created_at = models.DateTimeField()
	proctorNotes = models.TextField()
	sessionNotes = models.TextField()


class Participant(models.Model):
	name = models.TextField()
	role = models.ForeignKey(Role)


class Score(models.Model):
	events_failed = models.ManyToManyField(Event)
	events_succeeded = models.ManyToManyField(Event)
	quant_score = models.DecimalField()
	participant = models.ForeignKey(Participant)


class Action(models.Model):
	timestamp = models.DateTimeField()
	action_type = models.BooleanField() # catagory type
	participant = models.ForeignKey(Participant)
	quantity = models.IntegerField()
	resource = models.ManyToManyField(Resource)