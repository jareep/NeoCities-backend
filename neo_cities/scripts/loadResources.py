from neo_api.models import Resource
import json
import sys

with open(os.path.join(os.path.dirname(__file__), 'resources.json')) as f:
    resourceData = json.load(f)

for resource in resourceData["resources"]["resource"]:
    Resource.objects.create(id = resource["id"], name=resource["type"], icon=resource["icon"])
