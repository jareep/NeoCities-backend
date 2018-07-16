from django.contrib import admin
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action, ResourceEventState, ChatSession
from django.http import HttpResponse
import csv

def export_csv(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    for session in queryset:
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = f'attachment; filename="{session.sessionKey}-actions.csv"'

        writer = csv.writer(response)
        writer.writerow(["Scenario Title", "Action Type", "Quantity", "Participant Name" , "Event Description", "Time Stamp"])
        for action in session.action_set.all():
            writer.writerow([session.scenario_ran.title, action.action_type, action.quantity, action.participant.name , action.event.description, action.timestamp])

    return response
export_csv.short_description = "Export to CSV"

def export_messages(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    for chat_session in queryset:
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = f'attachment; filename="{chat_session.id}-{chat_session.session.sessionKey}-chat_session.csv"'

        writer = csv.writer(response)
        writer.writerow(["Chat Session ID", "Session Key", "Participant Name", "Message Text"])
        for message in chat_session.message_set.all():
            writer.writerow([chat_session.id, chat_session.session.sessionKey, message.participant.name,  message.text])

    return response
export_csv.short_description = "Export Messages to CSV's"

class SessionAdmin(admin.ModelAdmin):
    list_display = ['scenario_ran', 'sessionKey']
    ordering = ['id']
    actions = [ export_csv ]

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session']
    ordering = ['id']
    actions = [ export_messages ]

# Register your models here.
model_list = [Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Action, ResourceEventState]
for model in model_list:
    admin.site.register(model)
admin.site.register(Session, SessionAdmin)
admin.site.register(ChatSession, ChatSessionAdmin)
