# Topic Dynamic redis channel layer

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync

# Ex-01(SyncConsumer)
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket Connection....', event)
        print('Channel Layer :', self.channel_layer)    # get default channerl layer from a project
        print('Channel Name :', self.channel_name)      # get channel name
        
        
        # dynamic urls group name
        self.GROUP_NAME = self.scope['url_route']['kwargs']['usergroup']    # scope- user request information
        print('Group Name...', self.GROUP_NAME)               
        
        # create Group- add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'programmers',                              # Create group Name (static)
            self.GROUP_NAME,                              # Create group Name (dynamic)
            self.channel_name,
        )
        
        self.send({
            'type': 'websocket.accept',           # request accept
        })
    
    
    
    def websocket_receive(self, event):
        print('Message from client...', event)
        print('message from client to server...', event['text'])
        
        print('Type of message receive from client...', type(event['text']))
        
        
        # group message send access
        async_to_sync(self.channel_layer.group_send)(
            # 'programmers',                              # Create group Name (static)
            self.GROUP_NAME,                              # Create group Name (dynamic)
            {
                'type': 'chat.message',             # create event handler
                'message': event['text']
            }
        )
    
    # Frontend - passing client
    def chat_message(self, event):      # calling handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        self.send({
            'type': 'websocket.send',              # request send Frontend
            'text': event['message']
        })
        
    
    
    
    def websocket_disconnect(self, event):
        print('Websocket disconnected....', event)
        print('Channel Layer :', self.channel_layer)    # get default channerl layer from a project
        print('Channel Name :', self.channel_name)      # get channel name
        
        # create Group- disconnect a channel to a new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            # 'programmers',                                  # Create group Name (static)
            self.GROUP_NAME,                                    # Create group Name (dynamic)
            self.channel_name,
        )
        
        raise StopConsumer()
    
    
    
# Ex-02(AsyncConsumer)
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket Connection....', event)
        print('Channel Layer :', self.channel_layer)    # get default channerl layer from a project
        print('Channel Name :', self.channel_name)      # get channel name
        
        
        # dynamic urls group name
        self.GROUP_NAME = self.scope['url_route']['kwargs']['usergroup']    # scope- user request information
        print('Group Name...', self.GROUP_NAME)               
        
        # create Group- add a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'programmers',                              # Create group Name (static)
            self.GROUP_NAME,                              # Create group Name (dynamic)
            self.channel_name,
        )
        
        await self.send({
            'type': 'websocket.accept',           # request accept
        })
    
    
    
    async def websocket_receive(self, event):
        print('Message from client...', event)
        print('message from client to server...', event['text'])
        
        print('Type of message receive from client...', type(event['text']))
        
        
        # group message send access
        await self.channel_layer.group_send(
            # 'programmers',                              # Create group Name (static)
            self.GROUP_NAME,                              # Create group Name (dynamic)
            {
                'type': 'chat.message',             # create event handler
                'message': event['text']
            }
        )
    
    # Frontend - passing client
    async def chat_message(self, event):      # calling handler
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of actual data...', type(event['message']))
        
        await self.send({
            'type': 'websocket.send',              # request send Frontend
            'text': event['message']
        })
        
    
    
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnected....', event)
        print('Channel Layer :', self.channel_layer)    # get default channerl layer from a project
        print('Channel Name :', self.channel_name)      # get channel name
        
        # create Group- disconnect a channel to a new or existing group
        await self.channel_layer.group_discard(
            # 'programmers',                                  # Create group Name (static)
            self.GROUP_NAME,                                    # Create group Name (dynamic)
            self.channel_name,
        )
        
        raise StopConsumer()


