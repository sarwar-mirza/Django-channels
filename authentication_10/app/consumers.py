# Topic - Create consumer Authentication

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync
import json
from .models import Chat, Group

from channels.db import database_sync_to_async

# Ex-01(SyncConsumer)
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        # Debuging 
        print('Websocket connection...', event)
        print('Channel Layer...', self.channel_layer)      # get default channerl layer from a project
        print('Channel Name ...', self.channel_name)        # get channel name
        
        # dynamic urls group name
        self.GROUP_NAME = self.scope['url_route']['kwargs']['routingGroupName']    # scope- user request information
        print('Group Name...', self.GROUP_NAME) 
        
        # create Group- add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'programmers',                              # create group name(static)
            self.GROUP_NAME,                              # create group name(dynamic)
            self.channel_name,
        )
        
        self.send({
            'type': 'websocket.accept',     # request accept
        })
        
        
    def websocket_receive(self, event):
        print('Message from client...', event)
        print('Message receive from client...', event['text'])
        print('Type of message receive from client...', type(event['text']))
        
        # database information
        data = json.loads(event['text'])       # string to object convert
        print('Data...', data)
        print('Type of data....', type(data))
        print('Chat message data store...', data['msg'])
        print('User check....', self.scope['user'])
        # Find Group object
        group = Group.objects.get(name=self.GROUP_NAME)   # create dynamic group name
        
        if self.scope['user'].is_authenticated:         # Condition checke 

            # Create new chat object
            chat = Chat(
                content= data['msg'],
                model_group= group
            )
            chat.save()
            
            data['user'] = self.scope['user'].username      # with username
            print('complete data....', data)
            print('Type of complete data...', type(data))
            
            
            # group message send access
            async_to_sync(self.channel_layer.group_send)(
                # 'programmers',                              # Create group Name (static)
                self.GROUP_NAME,                              # create group name(dynamic)

                {
                    'type': 'chat.message',             # create event handler
                    # 'message': event['text']            # without username
                    'message': json.dumps(data)            # with username and python to string
                }
            )
        
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login required", "user":"Guest"})     # python to string
            })
        
    # Frontend - passing client
    def chat_message(self, event):      # calling handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })
        
        
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        print('Channel Layer...', self.channel_layer)      # get default channerl layer from a project
        print('Channel Name ...', self.channel_name)        # get channel name
        
        # create Group- disconnect a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'programmers',                              # create group name(static)
            self.GROUP_NAME,                              # create group name(dynamic)
            self.channel_name
        )
        raise StopConsumer()
    
    
    
    
    
    
# Ex-02(ASyncConsumer)
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        # Debuging 
        print('Websocket connection...', event)
        print('Channel Layer...', self.channel_layer)      # get default channerl layer from a project
        print('Channel Name ...', self.channel_name)        # get channel name
        
        # dynamic urls group name
        self.GROUP_NAME = self.scope['url_route']['kwargs']['routingGroupName']    # scope- user request information
        print('Group Name...', self.GROUP_NAME) 
        
        # create Group- add a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'programmers',                              # create group name(static)
            self.GROUP_NAME,                              # create group name(dynamic)
            self.channel_name,
        )
        
        await self.send({
            'type': 'websocket.accept',     # request accept
        })
        
        
    async def websocket_receive(self, event):
        print('Message from client...', event)
        print('Message receive from client...', event['text'])
        print('Type of message receive from client...', type(event['text']))
        
        # database information
        data = json.loads(event['text'])       # string to object convert
        print('Data...', data)
        print('Type of data....', type(data))
        print('Chat message data store...', data['msg'])
        print('User check....', self.scope['user'])
        
        

        # Find Group object
        group = await database_sync_to_async(Group.objects.get)(name=self.GROUP_NAME)   # create dynamic group name,   write in code exactly (ORM)

        
        if self.scope['user'].is_authenticated:         # Condition checke 
            
            # Create new chat object
            chat = Chat(
                content= data['msg'],
                model_group= group
            )
            await database_sync_to_async(chat.save)()      # write in code exactly (ORM)
            
            data['user'] = self.scope['user'].username      # with username
            print('complete data....', data)
            print('Type of complete data...', type(data))
            
            # group message send access
            await self.channel_layer.group_send(
                # 'programmers',                              # Create group Name (static)
                self.GROUP_NAME,                              # create group name(dynamic)

                {
                    'type': 'chat.message',             # create event handler
                    # 'message': event['text']            # without username
                    'message': json.dumps(data)            # with username and python to string
                }
            )
        
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login required", "user":"Guest"})
            })
    # Frontend - passing client
    async def chat_message(self, event):      # calling handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        await self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })
        
        
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        print('Channel Layer...', self.channel_layer)      # get default channerl layer from a project
        print('Channel Name ...', self.channel_name)        # get channel name
        
        # create Group- disconnect a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'programmers',                              # create group name(static)
            self.GROUP_NAME,                              # create group name(dynamic)
            self.channel_name
        )
        raise StopConsumer()