from django.db import models

# TODO Before hook to check that no session is active. If the session is active deny saving

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


# it might be worth to look into a more advance model that will allow things to change over time eventually
class Threshold(models.Model):
    # todo: see if we could use a special value like -1 to say order does not matter
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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, name="role")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, name="resource")


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
    # score should probably store role and session

class Session(models.Model):
    # We need to keep in mind that this could result in orphaned session
    # But these sessions are always needed for logging
    scenario_ran = models.ForeignKey(Scenario, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()
    proctorNotes = models.TextField(default="")
    sessionNotes = models.TextField(default="")


class Participant(models.Model):
    name = models.TextField()
    token = models.TextField()
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True)  # this should probably be under the session through role


class Action(models.Model):
    timestamp = models.DateTimeField()
    action_type = models.BooleanField()  # category type
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    resource = models.ManyToManyField(Resource) # todo: maybe the wrong relationship type
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
