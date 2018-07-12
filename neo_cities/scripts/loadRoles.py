from neo_api.models import Resource, Role, ResourceDepot
import json
import sys

with open(os.path.join(os.path.dirname(__file__), 'roles.json')) as f:
    roleData = json.load(f)

for role in roleData["roles"]["role"]:
    new_role = Role.objects.create(id = role["id"], name=role["type"], icon=role["logo"])
    for resource_id in role["resources"]:
        ResourceDepot.objects.create(role = new_role, resource = Resource.objects.get(id = resource_id), quantity = 2)
