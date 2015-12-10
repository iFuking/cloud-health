#!/bin/bash

# server host & working directory
REMOTE_HOST=wcm@172.18.9.7
REMOTE_DIR=/var/www/wechat/

# local working directory
WORKING_DIR=/home/dick/PycharmProjects/pyProject/

# ssh server & backup ${REMOTE_DIR}/python
ssh ${REMOTE_HOST} "sh ${REMOTE_DIR}script/bak_python.sh"

cd ${WORKING_DIR}
scp classify/recommend.py classify/wechat.py classify/classify.py classify/filter.py ${REMOTE_HOST}:${REMOTE_DIR}python
