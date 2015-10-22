#!/bin/bash
cd /home/dick/filter/
rm -r *
mkdir disease && mkdir drug && mkdir lore && mkdir news && mkdir symptom

cd /home/dick/PycharmProjects/pyProject/yi18_parse/
python drug.py && python general.py
