import asyncio,websockets,json

USERS = set() #set of WebSocketServerProtocol instances

DATA = {
    'users': {},  #dict of dicts: {uid: {name:   their chosen name,
                  #                      online: is there a websocket open with their uid,
                  #                      color:  their chosen colour}}
    'posts': []   #list of posts as objects: {uid: content}
}


def get_uid(websocket):
    'identifies the user'
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
    USERS.add(websocket)
    uid = get_uid(websocket)
    print(uid,'joined')
    if not uid in DATA['users']:
        await websocket.send(message_need_details())
        message = json.loads(await websocket.recv())
        assert message['type'] == 'update_details'
        update_details(uid,message['data'])
    DATA['users'][uid]['online']=1
    await broadcast_users()

async def handle_leave(websocket):
    USERS.remove(websocket)
    uid = get_uid(websocket)
    print(uid,'left')
    DATA['users'][uid]['online']=0
    await broadcast_users()

async def send_uid(websocket):
    uid = get_uid(websocket)
    await websocket.send(json.dumps({'type':'whoami','data':uid}))

async def handle_ws(websocket,path):
    uid = get_uid(websocket)
    await handle_join(websocket)
    await send_uid(websocket)
    await websocket.send(message_posts_update())
    try:
        async for message in websocket:
            message = json.loads(message)
            if message['type'] == 'update_details':
                update_details(uid,message['data'])
                await broadcast_users()
            elif message['type'] == 'new_message':
                DATA['posts'].append({'uid':uid,'content':message['data']})
                await broadcast_posts()
    finally:
        await handle_leave(websocket)

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(handle_ws,port=8000))
loop.run_forever()
