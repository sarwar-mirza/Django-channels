# Topic - channel layer chat app with static group name

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync
import json


# Ex-01(SyncConsumer)
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket connected....', event)
        print('Channels Layer :', self.channel_layer)     # get default channerl layer from a project
        
        print('Channel Name :', self.channel_name)        # get channel name
        
        # create Group- add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            'programmers',           # create group name (static)
            self.channel_name                    
            )
        
        self.send({
            'type': 'websocket.accept'
        })
    
    
    def websocket_receive(self, event):
        print('Message from receive...', event)
        print('Message from client...', event['text'])
    
        # receive message
        print('Type of message receive from client ', type(event['text']))
        
        async_to_sync(self.channel_layer.group_send)(
            'programmers',                     # Create group name (static)
            {
                'type': 'chat.message',                         # Create handler
                'message': event['text']
            }
        )
        
    # passing client (index.html) 
    def chat_message(self, event):            # calling handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect....', event)
        print('Channels Layer :', self.channel_layer)     # get default channerl layer from a project
        
        print('Channel Name :', self.channel_name)        # get channel name
        
        async_to_sync(self.channel_layer.group_discard)(
            'programmers',                                # Create group name (static)
            self.channel_name
            )
        raise StopConsumer()




# Ex-02(AsyncConsumer)
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket Connect....', event)
        print('Channels Layer :', self.channel_layer)     # get default channerl layer from a project
        
        print('Channel Name :', self.channel_name)        # get channel name
        
        # create Group- add a channel to a new or existing group
        
        await self.channel_layer.group_add(
            'programmers',                   # Create group name (static)
            self.channel_name
            )

        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        print('Message from client...', event)
        print('message from client to server...', event['text'])
        
        # receive message
        print('Type of receive message from client...', type(event['text']))
        
        # paccing frontend(index.html)
        await self.channel_layer.group_send(
            'programmers',                          # Create group name (static)
            {
                'type': 'chat.message',             # create Event handler
                'message': event['text']
            }
        )
    
    async def chat_message(self, event):            # receive handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
    
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        print('channels layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)
        
        await self.channel_layer.group_discard(
            'programmers',                          # Create group name (static)
            self.channel_name
            )
        raise StopConsumer()