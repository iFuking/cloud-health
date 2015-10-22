#!/bin/bash

cd /home/dick/classify/
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

cd /home/dick/PycharmProjects/pyProject/yi18_classify/
python drug.py && python general.py
