import asyncio,websockets,json

global w

async def handler(websocket,path):
    w = websocket    
    print('sending message')
    websocket.send('meow')
    async for message in websocket:
        websocket.send(message)

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(handler,port=8000))
loop.run_forever()
