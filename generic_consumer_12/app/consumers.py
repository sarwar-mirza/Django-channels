# Generic topic - Websocket Consumer, Async websocket consumer


from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from asgiref.sync import async_to_sync
import json
from .models import Chat, Group
from channels.db import database_sync_to_async


# Ex-01 (SyncConsumer)
class MyWebsocketConsumer(WebsocketConsumer):
    
    
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
        
        # Dynamic url 
        self.Consumer_GroupName = self.scope['url_route']['kwargs']['routingGroupName']      # scope- user request information
        print('Group Name....', self.Consumer_GroupName)
        
        # create Group- add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            self.Consumer_GroupName,          # Create dynamic Group name
            self.channel_name
        )
        self.accept()                           # To accept the connection
    
    
    
    # This handler is called when data received form client
    def receive(self, text_data=None, bytes_data=None):
        print('Message receive from client....', text_data)
        print('Type of message receive from client...', type(text_data))
        
        data = json.loads(text_data)       # string to python 
        print('Type of data...', type(data))
        print('Actual data....', data['msg'])
        
        # Database information
        group = Group.objects.get(name=self.Consumer_GroupName)    # Get create dynamic group name
        
        # Check user authenticated
        if self.scope['user'].is_authenticated:
        
            chat = Chat(
                content= data['msg'],
                model_group= group,
            )
            chat.save()
            
            
            
            async_to_sync(self.channel_layer.group_send)(
                self.Consumer_GroupName,               # create dynamic group name
                {
                    'type': 'chat.message',         # create event handler
                    'message': data['msg']          # without username
                }    
            )
        
        else:
            self.send(text_data=json.dumps({     # python to string
                "msg": "Login Required"
            }))
        
    
            
    
    # Frontend-  calling create event handler
    def chat_message(self, event):
        print('Event...', event)
        print('Actual data...', event['message'])
        
        print('type of actual data...', type(event['message']))
        
        self.send(json.dumps({                  # python to string
            'msg': event['message']
        }))
        
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    
    def disconnect(self, close_code):
        print('Websocket diconnect....', close_code)
        
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('Channel Name...', self.channel_name)         # get channel name
        
        # create Group- discard channel to a new or existing group
        self.channel_layer.group_discard(
            self.Consumer_GroupName,          # Create dynamic Group name
            self.channel_name
        )
        
        


# Ex-02 (AsyncConsumer) 
class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    
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
        print('channel Name...', self.channel_name)         # get channel name
        
        
        # Dynamic url 
        self.Consumer_GroupName = self.scope['url_route']['kwargs']['routingGroupName']      # scope- user request information
        print('Group Name....', self.Consumer_GroupName)
        
        # create Group- discard a channel to a new or existing group
        await self.channel_layer.group_add(
            self.Consumer_GroupName,           # create group name
            self.channel_name
        )
        
        await self.accept()                           # To accept the connection
    
    
    
    # This handler is called when data received form client
    async def receive(self, text_data=None, bytes_data=None):
        print('Message receive from client....', text_data)
        print('Type of message receive from client...', type(text_data))
        
        data = json.loads(text_data)       # string to python 
        print('Type of data...', type(data))
        print('Actual data....', data['msg'])
        
        # Database information
        group = await database_sync_to_async(Group.objects.get)(name=self.Consumer_GroupName)    # Get create dynamic group name. write in code exactly (ORM)
        
        # Authentication required
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content= data['msg'],
                model_group= group,
            )
            await database_sync_to_async(chat.save)()    # write in code exactly (ORM)
            
            await self.channel_layer.group_send(
                self.Consumer_GroupName,               # create dynamic group name
                {
                    'type': 'chat.message',         # create event handler
                    'message': data['msg']
                }
            )
        
        else:
            await self.send(text_data=json.dumps({     # python to string
                "msg": "Login Required"
            }))
    
    # Frontend-  calling create event handler
    async def chat_message(self, event):
        print('Event...', event)
        print('Actual data...', event['message'])
        
        print('type of actual data...', type(event['message']))
        
        await self.send(json.dumps({                  # python to string
            'msg': event['message']
        }))
        
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    
    async def disconnect(self, close_code):
        print('Websocket diconnect AsyncConsumer....', close_code)
        print('Channel Layer...', self.channel_layer)       # get default channerl layer from a project
        print('channel Name...', self.channel_name)         # get channel name
        
        # create Group- discard a channel to a new or existing group
        await self.channel_layer.group_discard(
            self.Consumer_GroupName,          # Create dynamic Group name
            self.channel_name
        )