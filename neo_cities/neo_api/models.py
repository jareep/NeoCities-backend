from django.db import models

# Create your models here.

class Resource(models.Model):
    name = models.TextField()
    icon = models.FileField(upload_to='icons/')

    def __str__(self):
     return self.name


class Event(models.Model):
    # TODO : Event Name Field & update in Test
    success_resources = models.ManyToManyField(Resource, through='Threshold')
    icon = models.FileField(upload_to='icons/events/')
    start_time = models.TimeField()
    description = models.TextField()
    details = models.TextField()

    def __str__(self):
     return self.description


# it might be worth to look into a more advance model that will allow things to change over time eventually
class Threshold(models.Model):
    # todo: see if we could use a special value like -1 to say order does not matter
    order = models.IntegerField()
    amount = models.IntegerField()
    enforce_order = models.BooleanField(default=False)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
     return "{self.event} Needs {self.resource}"


class Role(models.Model):
    name = models.TextField()
    icon = models.FileField(upload_to='icons/roles/')
    resources = models.ManyToManyField(Resource, through='ResourceDepot')

    def __str__(self):
     return self.name


class ResourceDepot(models.Model):
    quantity = models.IntegerField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, name="role")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, name="resource")

    def __str__(self):
     return f"{self.role} has {self.quantity} {self.resource}"

class Scenario(models.Model):
    title = models.TextField()
    events = models.ManyToManyField(Event)
    roles = models.ManyToManyField(Role)

    def __str__(self):
     return f"Scenario {self.id}"

class Briefing(models.Model):
    details = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
     return f"Briefing for {self.role} in {self.scenario}"

# Logging Info

class Score(models.Model):
    quant_score = models.DecimalField(decimal_places=2, max_digits=5)
    # score should probably store role and session

class Session(models.Model):
    # We need to keep in mind that this could result in orphaned session
    # But these sessions are always needed for logging
    sessionKey = models.CharField(max_length=40, unique=True)
    scenario_ran = models.ForeignKey(Scenario, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()
    proctorNotes = models.TextField(default="")
    sessionNotes = models.TextField(default="")

    def __str__(self):
        return f"Created: {self.created_at} SessionKey: {self.sessionKey}"


class ChatSession(models.Model):
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)

class Participant(models.Model):
    name = models.TextField()
    token = models.CharField(max_length=40, unique=True)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True)  # this should probably be under the session through role
    chat_session = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True)

    def __str__(self):
     return self.name

class Message(models.Model):
    text = models.TextField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)

class Action(models.Model):
    timestamp = models.DateTimeField()
    action_type = models.CharField(max_length=6)  # category type, DEPLOY, RECALL
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    resource = models.ForeignKey(Resource, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)

class ResourceEventState(models.Model):
    success = models.BooleanField(default=False)
    deployed = models.IntegerField(default=0)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
