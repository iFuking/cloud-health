#!/bin/bash

IMAGE_PATH='/home/dick/PycharmProjects/pyProject/image/apk_img'
cd ${IMAGE_PATH}

for i in {1..1110}
do
		convert ${i}.png ${i}.jpg
done
