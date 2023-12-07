# Topic Create consumer Handle websocket from websocket javaScript

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket connect ...', event)
        
        self.send({
            'type': 'websocket.accept'                        # websocket accept
        })
    
    def websocket_receive(self, event):
        print('Message receive ...', event)
        print('message from client ', event['text'])
        
        for i in range(10):
            self.send({
                'type': 'websocket.send',                     # websocket send
                'text': str(i)
            })
            sleep(1)
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect ...', event)
        raise StopConsumer()
    
    
    
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket connect ...', event)
        
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        print('Message receive ...', event)
        print('message from client ', event['text'])
        
        for i in range(10):
            await self.send({
                'type': 'websocket.send',
                'text': str(i)
            })
            asyncio.sleep(1)
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnect ...', event)
        raise StopConsumer()
