#!/bin/bash

FILTER_PATH='/home/dick/filter/'
cd ${FILTER_PATH}
rm -r *
mkdir disease && mkdir drug && mkdir lore && mkdir news && mkdir symptom

RUN_PATH='/home/dick/PycharmProjects/pyProject/yi18_parse/'
cd ${RUN_PATH}
python drug.py && python general.py
