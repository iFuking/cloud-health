#!/bin/bash

WORKING_DIR=/var/www/wechat/

cd ${WORKING_DIR}
mv python/wechat.py bak_python/wechat$(date "+%Y-%m-%d_%H:%M:%S").py
