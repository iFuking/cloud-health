#!/bin/bash

CLASSIFY_PATH='home/dick/classify/'
cd ${CLASSIFY_PATH}
rm -r *

for class in bp fat cold back digest pee
do
		mkdir $class
		cd $class
		for item in disease drug lore news symptom
		do
				mkdir $item
		done
		cd ..
done

RUN_PATH='/home/dick/PycharmProjects/pyProject/yi18_classify/'
cd ${RUN_PATH}
python drug.py && python general.py
