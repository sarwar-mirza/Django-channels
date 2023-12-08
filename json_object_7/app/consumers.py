# Topic Create consumer 
'''
backend:
python to string => json.dumps(variable_name)
string to python => json.loads(variable_name)

frontend:
string to javascript object => JSON.parse(variable_name)
javascript object to string => JSON.stringfy(variable_name)
'''
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket connect...', event)
        
        self.send({
            'type': 'websocket.accept'               # request accept
        })
    
    def websocket_receive(self, event):
        print('Message receive...', event)
        print('message from client ', event['text'])
        
        for i in range(10):
            self.send({
                'type': 'websocket.send',            # request send
                'text': json.dumps({"count": i})      # (convert)-python to string
            })
            sleep(1)
    
    def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()
    
    
    
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket connect...', event)
        
        await self.send({
            'type': 'websocket.accept'               # request accept
        })
    
    async def websocket_receive(self, event):
        print('Message receive...', event)
        print('message from client ', event['text'])
        
        for i in range(20):
            await self.send({
                'type': 'websocket.send',            # request send
                'text': str(i)
            })
            await asyncio.sleep(1)
    
    async def websocket_disconnect(self, event):
        print('Websocket disconnect...', event)
        raise StopConsumer()


