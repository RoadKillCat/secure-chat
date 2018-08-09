secure chat
===========

#### A simple chat webapp using WebSockets

---

### Installation

To host yourself:

 - clone this repo
 - navigate to it
 - install with

```shell
sudo ./install.sh
```

and uninstalling is as simple as:

```shell
sudo ./uninstall.sh
```

---

### Usage

*All server commands must be made with super user privileges (either prefix with `sudo` or run `sudo su` first to switch to root).*

To start the server, run:

```shell
chat_server start
```
and then visit the server's IP address to use the chat app.

To see the status of the html and websocket servers, use

```shell
chat_server status
```

which merely echoes the calls to `systemctl status`.

To stop the server, run:

```shell
chat_server stop
```
