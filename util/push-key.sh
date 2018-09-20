#!/bin/bash

PORT=22

if [ ! -f ~/.ssh/id_rsa.pub ]; then
    ssh-keygen -t rsa
fi

cat ~/.ssh/id_rsa.pub | ssh -p $PORT $1 "
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cat >> ~/.ssh/authorized_keys
    sort -u ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.bak
    mv ~/.ssh/authorized_keys.bak ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
"

ssh -p $PORT -n -o PasswordAuthentication=no $1 true
