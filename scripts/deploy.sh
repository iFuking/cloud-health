#!/bin/bash

# server host & working directory
REMOTE_HOST=wcm@172.18.9.7
REMOTE_DIR=/var/www/wechat/

# local working directory
WORKING_DIR=/home/dick/PycharmProjects/pyProject/

# ssh server & backup ${REMOTE_DIR}/python
echo "backup files..."
ssh ${REMOTE_HOST} "sh ${REMOTE_DIR}script/bak_python.sh"

cd ${WORKING_DIR}
echo "upload files..."
scp classify/wechat.py ${REMOTE_HOST}:${REMOTE_DIR}python
