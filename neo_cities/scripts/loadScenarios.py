from neo_api.models import Resource, Role, Scenario, Event, Threshold
import json
import sys

with open(os.path.join(os.path.dirname(__file__), 'scenarios.json')) as f:
    scenarioData = json.load(f)["scenario"]

scenario = Scenario.objects.create(title = scenarioData["title"])

for event in scenarioData["events"]:
    new_event = Event.objects.create(id = event["event_id"],
        icon = event["icon"], description = event["description"], details = event["details"], start_time = event["start_time"])
    for threshold in event["answer"]:
        Threshold.objects.create(enforce_order = event["enforce_resource_order"],
        resource = Resource.objects.get(id = threshold["resource_id"]), amount = event["num_needed"], event = new_event)
