#~/bin/bash

WORKING_DIR=/var/www/wechat/
cd ${WORKING_DIR}

python python/recommend.py && python python/wechat.py
