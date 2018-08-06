#! /bin/bash

#directories (name of program `server` is fixed)
DAEMON_DIR='/etc/systemd/system'
BIN_DIR='/usr/local/bin'

echo "installing secure_chat server"
echo "copying daemon files to $DAEMON_DIR"
sudo cp *.service $DAEMON_DIR
echo "creating symbolic link to server shell script in $BIN_DIR"
sudo ln -s $(pwd)/server $BIN_DIR/server
echo "install complete"
