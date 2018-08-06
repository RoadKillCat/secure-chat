#! /bin/bash

#directories (name of program `server` is fixed)
DAEMON_DIR='/etc/systemd/system'
BIN_DIR='/usr/local/bin'

echo "uninstalling secure_chat server"
echo "removing daemon files in $DAEMON_DIR"
for f in *.service; do
    sudo rm $DAEMON_DIR/$f
done

echo "removing symbolic link to server shell script in $BIN_DIR"
sudo rm $BIN_DIR/server
echo "uninstall complete"
