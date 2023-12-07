# Topic Consumer Create detail 

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket Connect...', event)
        
        self.send({
            'type': 'websocket.accept',
        })
    
    
    def websocket_receive(self, event):
        print('Message receive...', event)
        print('message from client ', event['text'])
        
        self.send({
            'type': 'websocket.send',
            'text': 'thanks for website visit'
        })
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()
    
    
    
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket Connect...', event)
        
        await self.send({
            'type': 'websocket.accept',
        })
    
    
    async def websocket_receive(self, event):
        print('Message receive...', event)
        print('message from client ', event['text'])
        
        await self.send({
            'type': 'websocket.send',
            'text': 'thanks for website visit'
        })
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()


