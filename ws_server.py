import asyncio,websockets,json,hashlib

USERS = set() #set of WebSocketServerProtocol instances

DATA = {
    'users': {},  #dict of dicts: {uid: {name:   their chosen name,
                  #                      online: is there a websocket open with their uid,
                  #                      color:  their chosen colour}}
    'posts': []   #list of posts as objects: {uid: content}
}

PASSKEY = '02edbb53017ded13c286e27d14285cb82f5a87f6dcbae280d6c53b5d98477bb7'

def get_uid(websocket):
    ip,port = websocket.remote_address
    #return hashlib.sha1(ip.endcode('utf-8'))[:5]
    return ip

def message_users_update():
    return json.dumps({'type':'users_update', 'data': DATA['users']})

def message_posts_update():
    return json.dumps({'type':'posts_update', 'data': DATA['posts']})

def message_need_details():
    return json.dumps({'type':'need_details'})

async def broadcast_posts():
    print('broadcasting_posts')
    if not USERS: return
    await asyncio.wait([user.send(message_posts_update()) for user in USERS])

async def broadcast_users():
    print('broadcasting_users')
    if not USERS: return
    await asyncio.wait([user.send(message_users_update()) for user in USERS])

def update_details(uid,details):
    DATA['users'].setdefault(uid,{}).update(details)

async def handle_join(websocket):
    print(websocket.uid,'joined')
    if not websocket.uid in DATA['users']:
        await websocket.send(message_need_details())
        try:
            message = json.loads(await websocket.recv())
        except websockets.exceptions.ConnectionClosed:
            return False
        assert message['type'] == 'update_details'
        update_details(websocket.uid,message['data'])
    USERS.add(websocket)
    DATA['users'][websocket.uid]['online']=1
    await broadcast_users()
    return True

async def handle_leave(websocket):
    print(websocket.uid,'left')
    USERS.remove(websocket)
    DATA['users'][websocket.uid]['online']=0
    await broadcast_users()

async def send_uid(websocket):
    await websocket.send(json.dumps({'type':'whoami','data':websocket.uid}))

async def authenticate(websocket):
    message = json.loads(await websocket.recv())
    assert message['type'] == 'authenticate'
    success = hashlib.sha256(message['data'].encode('utf-8')).hexdigest() == PASSKEY
    print(websocket.uid,'passed' if success else 'failed ('+message['data']+')','authetication')
    await websocket.send(json.dumps({'type':'authenticate','data':success}))
    return success

async def handle_ws(websocket,path):
    try:
        websocket.uid = get_uid(websocket)
        print(websocket.uid,'connected')
        if not await authenticate(websocket):
            await websocket.close()
            return
        if not await handle_join(websocket): return
        await send_uid(websocket)
        await websocket.send(message_posts_update())
    except:
        print('caught something')
    try:
        async for message in websocket:
            message = json.loads(message)
            if message['type'] == 'update_details':
                update_details(websocket.uid,message['data'])
                await broadcast_users()
            elif message['type'] == 'new_message':
                DATA['posts'].append({'uid':websocket.uid,'content':message['data']})
                await broadcast_posts()
    finally:
        await handle_leave(websocket)

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(handle_ws,port=8000))
loop.run_forever()
