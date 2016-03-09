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
scp wechat_recommand/wechat.py wechat_recommand/filter.py wechat_recommand/init.py wechat_recommand/recommend.py wechat_recommand/apk.py wechat_recommand/classify.py wechat_recommand/wx_group.py ${REMOTE_HOST}:${REMOTE_DIR}python
