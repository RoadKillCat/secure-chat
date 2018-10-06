secure chat
===========

#### A simple chat webapp using WebSockets

This was just a simple project to test the capabilities of websockets (and their secure `wss` counterparts).

Prior to using websockets, I was using basic HTTP requests. I tried two methods: having the client poll the server for new messages (which was bad since that's a lot of unnecessary network traffic) and hanging GET requets (where the user asks for the next new message and the server doesn't repsond until it recieves a new message from a different client). Both these methods were inferior to the beauty of websockets which allow for full duplex communication with really small latency (~20ms on my machine).

Get some friends (since its unlikely I'll have it open when your reading this) and go to https://joeiddon.github.io/secure_chat to try it out.

The websocket server code and client HTML script is available in this repo, and if you view the commit history, you can look back to the older HTTP request code if you are interested (beware, my commit messages are unhelpful and the code is pretty hacky back there!).
