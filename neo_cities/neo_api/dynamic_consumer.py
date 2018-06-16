from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class DynamicConsumer(JsonWebsocketConsumer):
    groups = ["participants"]
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connect(self, **kwargs):
        """
        Perform things on connection start
        """
        self.accept()
        async_to_sync(self.channel_layer.group_add)("participants", self.channel_name)

    def receive_json(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        http_user = True

    def send_json(self, content):
        self.send(json.dumps(content))


    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass
