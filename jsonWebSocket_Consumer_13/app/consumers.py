# Generic Consumer- JsonWebSocket and AsyncjsonWebSocket consumer

from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from app.models import Chat, Group
import json

from channels.db import database_sync_to_async

# Ex-01(SyncConsumer)
class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    
    '''
    This handler is called when client initally opens a 
    connection and is about to finish the websocket handshake.
    
    self.accept() -To accept the connection
    self.close() - To reject the  connection. this functon is used any endig point
    self.close(code=4123) - TO add a custom websocket error code 
    '''
    def connect(self):
        print('Websocket connection SyncConsumer.....')
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('Channel Name...', self.channel_name)         # get channel name
        
        # get group name syntax variable_declar = self.scope['url_route']['kwargs']['routingGroupName']
        self.Consumer_GroupName = self.scope['url_route']['kwargs']['routingGroupName']     # scope- user request information
        print('Group Name....', self.Consumer_GroupName)
        
        # create Group- add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            self.Consumer_GroupName,                        # Create dynamic group name
            self.channel_name
        )
        
        self.accept()       # To accept the connection
        
    
    # This handler is called when data received form client
    # with decoded JSON content
    def receive_json(self, content, **kwargs):
        print('Message receive from client....', content)
        print('Actual message from client...', content['msg'])

        
        # Database- models.py
        group = Group.objects.get(name=self.Consumer_GroupName)
        
        # Check user authentication
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content= content['msg'],
                model_group= group
            )
            
            chat.save()
            
            
            # Show messages from clients sending your group messages
            async_to_sync(self.channel_layer.group_send)(
                self.Consumer_GroupName,
                {
                    'type': 'chat.message',                 # create event handler
                    'message': content['msg']
                    
                }
            )
        
        else:
            self.send_json({
                'msg_consumer': 'Login Required'
            })
    
    # Frontend-  calling create event handler
    def chat_message(self, event):
        print('Event....', event)
        print('Actual data...', event['message'])
        print('type of actual data...', type(event['message']))
        
        self.send_json({                            # Frontend- send ws.onmessage  event(display)
            'msg_consumer': event['message']
        })
    
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    def disconnect(self, close_code):
        print('Websocket disconnect SyncConsumer.....', close_code)
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('Channel Name...', self.channel_name)         # get channel name
        
        # create Group- discard a channel to a new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            self.Consumer_GroupName,                        # Create dynamic group name
            self.channel_name
        )


# Ex-02(AsyncConsumer)
class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    
    '''
    This handler is called when client initally opens a 
    connection and is about to finish the websocket handshake.
    
    self.accept() -To accept the connection
    self.close() - To reject the  connection. this functon is used any endig point
    self.close(code=4123) - TO add a custom websocket error code 
    '''
    async def connect(self):
        print('Websocket connection AsyncConsumer.....')
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('Channel Name...', self.channel_name)         # get channel name
        
        self.Consumer_GroupName = self.scope['url_route']['kwargs']['routingGroupName']     # scope- user request information
        print('Group Name....', self.Consumer_GroupName)
        
        # create Group- add a channel to a new or existing group
        await self.channel_layer.group_add(
            self.Consumer_GroupName,                        # Create dynamic group name
            self.channel_name
        )
        
        await self.accept()       # To accept the connection
        
    
    # This handler is called when data received form client
    # with decoded JSON content
    async def receive_json(self, content, **kwargs):
        print('Message receive from client....', content)
        print('Actual message from client...', content['msg'])

        
        # Database- models.py
        group = await database_sync_to_async(Group.objects.get)(name=self.Consumer_GroupName)   # Get create dynamic group name. write in code exactly(ORM)
        
        # Check user authentication
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content= content['msg'],
                model_group= group
            )
            
            await database_sync_to_async(chat.save)()   # write in code exactly(ORM)
            
            
            # Show messages from clients sending your group messages
            await self.channel_layer.group_send(            
                self.Consumer_GroupName,
                {
                    'type': 'chat.message',                 # create event handler
                    'message': content['msg']
                    
                }
            )
        
        else:
            await self.send_json({
                'msg_consumer': 'Login Required'
            })
    
    # Frontend-  calling create event handler
    async def chat_message(self, event):
        print('Event....', event)
        print('Actual data...', event['message'])
        print('type of actual data...', type(event['message']))
        
        await self.send_json({                            # Frontend- send ws.onmessage  event(display)
            'msg_consumer': event['message']
        })
    
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    async def disconnect(self, close_code):
        print('Websocket disconnect AsyncConsumer.....', close_code)
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('Channel Name...', self.channel_name)         # get channel name
        
        # create Group- discard a channel to a new or existing group
        await self.channel_layer.group_discard(
            self.Consumer_GroupName,                        # Create dynamic group name
            self.channel_name
        )