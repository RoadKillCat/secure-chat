'use strict';
let entry = document.getElementById('entry');
let out   = document.getElementById('out');
let num_msgs = 0;
let send = function(content){
    let xhr = new XMLHttpRequest();
    xhr.open('POST','');
    xhr.send(content);
}
send('i joined');
window.onbeforeunload = function(){
    send('i left');
    return '';
}
entry.onkeyup = function(e){
    if(e.keyCode==13){
        send(entry.value);
        entry.value='';
    }
}
let get_new_messages = function(){
    let xhr = new XMLHttpRequest();
    xhr.open('GET','/new_messages');
    xhr.setRequestHeader('num_msgs', num_msgs);
    xhr.send();
    xhr.onload /*onreadystatechange*/ = function(){
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
//0   UNSENT            Client has been created. open() not called yet.
//1   OPENED            open() has been called.
//2   HEADERS_RECEIVED  send() has been called, and headers and status are available.
//3   LOADING           Downloading; responseText holds partial data.
//4   DONE              The operation is com
