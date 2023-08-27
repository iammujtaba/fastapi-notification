from fastapi import  WebSocket
from fasnof.cache import cache
import json
from notifications.models import UserNotificationService

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[int,WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.check_for_any_unpublished_communication(user_id)

    def disconnect(self, user_id:int):
        self.active_connections.pop(user_id,None)

    async def send_notification_to_client(self, user_id: int, message: str):
        if user_id not in self.active_connections:
            return self.publish_delayed_communication(user_id,message)

        if self.active_connections.get(user_id):
            await self.active_connections[user_id].send_text(message)

    async def broadcast_notification(self, user_id:int,message: str):
        if user_id not in self.active_connections:
            return self.publish_delayed_communication(user_id,message)

        for connection,websocket in self.active_connections.items():
            if connection != user_id:
                await websocket.send_text(message)

    def publish_delayed_communication(self,user_id:int,message:str):
        existing_msgs = cache.get(f"ws-{user_id}") or []
        if isinstance(existing_msgs,bytes):
            existing_msgs = json.loads(existing_msgs)
        existing_msgs.append(message)
        cache.set(f"ws-{user_id}",json.dumps(existing_msgs),expire_time=60*60*24) #default timeout 1day we can change it later

    async def check_for_any_unpublished_communication(self,user_id:int):
        existing_msgs = cache.get(f"ws-{user_id}") or []
        if existing_msgs:
            for msg in json.loads(existing_msgs):
                await self.send_notification_to_client(user_id,msg)
            cache.delete(f"ws-{user_id}")

class EventLogger:
    def __init__(self,process_event:bool=False):
        self.process_event = process_event
        if self.process_event:
            self.ws_client = websocker_manager

    def create_event_db_entry(self,event_name:str,content:dict):
        content['event_name'] = event_name
        UserNotificationService().create(**content) # creating database entry for the event

    async def log_event(self, event_name:str, content:dict):

        if self.process_event:
            user_id = content.get('user_id')
            if not user_id:
                raise ValueError("user_id is required to process event")
            self.create_event_db_entry(event_name,content)
            await self.ws_client.send_notification_to_client(int(user_id),f"Event Name: {event_name}, Content: {content}")


websocker_manager = WebSocketManager()
event_logger = EventLogger(process_event=True)