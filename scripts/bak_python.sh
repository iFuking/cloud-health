#!/bin/bash

WORKING_DIR=/var/www/wechat/

cd ${WORKING_DIR}
mv python/recommend.py bak_python/recommend$(date "+%Y-%m-%d_%H:%M:%S").py
mv python/wechat.py bak_python/wechat$(date "+%Y-%m-%d_%H:%M:%S").py
mv python/classify.py bak_python/classify$(date "+%Y-%m-%d_%H:%M:%S").py
mv python/filter.py bak_python/filter$(date "+%Y-%m-%d_%H:%M:%S").py
