# Topic Courser create

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket connect...', event)
        
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print('Message receive...', event)
        print('message is ', event['text'])
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()
        
        
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket connect...', event)
        
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        print('Message receive...', event)
        print('message is ', event['text'])
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()


