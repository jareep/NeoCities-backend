from django.db import models


# Create your models here.

class Resource(models.Model):
    name = models.TextField()
    icon = models.FileField(upload_to='icons/')


class Event(models.Model):
    # TODO : Event Name Field & update in Test
    success_resources = models.ManyToManyField(Resource, through='Threshold')
    icon = models.FileField(upload_to='icons/events/')
    start_time = models.DateTimeField()
    description = models.TextField()
    details = models.TextField()


class Threshold(models.Model):
    order = models.IntegerField()
    amount = models.IntegerField()
    enforce_order = models.BooleanField(default=False)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Role(models.Model):
    name = models.TextField()
    icon = models.FileField(upload_to='icons/roles/')
    resources = models.ManyToManyField(Resource, through='ResourceDepot')


class ResourceDepot(models.Model):
    quantity = models.IntegerField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


class Scenario(models.Model):
    events = models.ManyToManyField(Event)
    roles = models.ManyToManyField(Role)


class Briefing(models.Model):
    details = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)


# Logging Info


class Score(models.Model):
    quant_score = models.DecimalField(decimal_places=2, max_digits=5)


class Participant(models.Model):
    name = models.TextField()
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)  # this should probably be under the session through role


class Session(models.Model):
    # We need to keep in mind that this could result in orphaned session
    # But these sessions are always needed for logging
    scenario_ran = models.ForeignKey(Scenario, null=True, on_delete=models.SET_NULL)
    session_token = models.TextField()
    participants = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()
    proctorNotes = models.TextField()
    sessionNotes = models.TextField()


class Action(models.Model):
    timestamp = models.DateTimeField()
    action_type = models.BooleanField()  # category type
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    resource = models.ManyToManyField(Resource)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
