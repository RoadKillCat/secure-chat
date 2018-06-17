'use strict';

let message_div = document.getElementById('out');
let demand_div  = document.getElementById('demand');
let details_but = document.getElementById('details_but');
let entry_input = document.getElementById('entry');
let name_input  = document.getElementById('name');
let col_input   = document.getElementById('col');

let ws_server = 'ws://35.207.51.171:8000/';
let known_user = 1; //assuming has logged on before
let my_uid;
let users;
let posts;
let num_posts = 0;

let websocket = new WebSocket(ws_server);

websocket.onmessage = function(e){
    let message = JSON.parse(e.data);
    switch (message['type']){
        case 'whoami':
            my_uid = message['data'];
            if (!users.length) console.log('sequencing err');
            name_input.value = users[my_uid].name;
            col_input.value  = users[my_uid].col;
            break;
        case 'need_details':
            known_user = 0;
            break;
        case 'users_update':
            users = message['data'];
            break;
        case 'posts_update':
            posts = message['data'];
            console.log(posts);
            break;
        default:
            console.log('unknown message type');
    }
}

details_but.onclick = function(){
    let message = {
        type: 'update_details',
        data: {'name': name_input.value,
               'col':  col_input.value}
    }
    websocket.send(JSON.stringify(message));
    known_user = 1;
    demand_div.style.display = 'none';
}

function send_message(s){
    if (!known_user){
        demand_div.style.display = 'block';
    } else {
        let message = {
            type: 'new_message',
            data: entry_input.value
        }
        websocket.send(JSON.stringify(message));
    }
}

entry_input.onkeyup = function(e){
    if(e.keyCode==13){
        send_message(entry_input.value);
        entry_input.value='';
    }
}
col_input.oninput = e=> col_input.style.color=col_input.value;

/*
function draw_messages(messages){
    for (;num_msgs<messages.length;num_msgs++){
            let msg = data['messages'][num_msgs];
            let uid = msg['uid']
            let el = document.createElement('div')
            el.style.color = data['users'][uid].color;
            if (uid == '364501') el.style.fontWeight = 'bold';
            el.innerText = msg['text'];
            out.appendChild(el);
        }
        document.title = messages[num_msgs-1]['content'];
        document.body.scrollTop = document.body.scrollHeight;
}
*/
/*
let get_new_messages = function(){
    let xhr = new XMLHttpRequest();
    xhr.open('GET','/new_messages');
    xhr.setRequestHeader('num_msgs', num_msgs);
    xhr.send();
    xhr.onload  = function(){
        console.log('xhr.readyState',xhr.readyState);
        let data = JSON.parse(xhr.responseText);
        let is_new = num_msgs < data['messages'].length;
        for (num_msgs; num_msgs < data['messages'].length; num_msgs++){
            let msg = data['messages'][num_msgs];
            let uid = msg['uid']
            let el = document.createElement('div')
            el.style.color = data['users'][uid].color;
            if (uid == '364501') el.style.fontWeight = 'bold';
            el.innerText = msg['text'];
            out.appendChild(el);
        }
        document.title = data['messages'][num_msgs-1]['text'];
        document.body.scrollTop = document.body.scrollHeight;
        get_new_messages();
    };
}
get_new_messages();
*/
