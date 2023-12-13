# Generic topic - Websocket Consumer, Async websocket consumer


from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from time import sleep
import asyncio

class MyWebsocketConsumer(WebsocketConsumer):
    
    
    '''
    This handler is called when client initally opens a 
    connection and is about to finish the websocket handshake.
    
    self.accept() -To accept the connection
    self.close() - To reject the  connection. this functon is used any endig point
    self.close(code=4123) - TO add a custom websocket error code 
    '''
    
    def connect(self):
        print('Websocket connection.....')
        self.accept()                           # To accept the connection
    
    
    
    # This handler is called when data received form client
    def receive(self, text_data=None, bytes_data=None):
        print('Message from client....', text_data)
        
        # To send data to client
        # self.send(text_data="Message from server to client")                #Ex-01 send message from server to client hardcode
        
        for i in range(20):                                                     #Ex-02 Real time data send
            self.send(str(i))
            sleep(1)
    
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    
    def disconnect(self, close_code):
        print('Websocket diconnect....', close_code)
        
        
        
        
        
        
class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    
    '''
    This handler is called when client initally opens a 
    connection and is about to finish the websocket handshake.
    
    self.accept() -To accept the connection
    self.close() - To reject the  connection. this functon is used any endig point
    self.close(code=4123) - TO add a custom websocket error code 
    '''
    
    async def connect(self):
        print('Websocket connection.....')
        await self.accept()                           # To accept the connection
    
    
    
    # This handler is called when data received form client
    async def receive(self, text_data=None, bytes_data=None):
        print('Message from client....', text_data)
        
        # To send data to client
        # await self.send(text_data="Message from server to client")            #Ex-01 send message from server to client hardcode
        
        for i in range(20):                                                     #Ex-02 Real time data send
            await self.send(str(i))
            await asyncio.sleep(1)
    
    
    '''
    This handler is called when either connection to the client is lost,
    either from the client closing the connection, the server
    closing the connection, or loss of the socket.
    '''
    
    async def disconnect(self, close_code):
        print('Websocket diconnect....', close_code)