#!/bin/bash

# working space directory, and change the directory
WORKSPACE_DIR=/home/dick/PycharmProjects/pyProject/
cd ${WORKSPACE_DIR}

# create yi18 database
python ./build_database_yi18/init.py

# import ./db_tables/*.sql files to yi18 database
# create yi18 database's tables
DATABASE_YI18=yi18
ITEM="ask book check disease drug food lore news surgery symptom"
for table in ${ITEM}
do
		mysql --user=root --password=123456 ${DATABASE_YI18} < ./db_tables/${table}.sql
done

# execute ./build_database_yi18/*.py python files
# build yi18 database's tables
for table in ${ITEM}
do
		python ./build_database_yi18/${table}.py
done



# create filter database
python ./build_database_classify/init_filter.py

# import ./filter_tables/*.sql files to filter database
# create filter database's tables
DATABASE_FILTER=filter
for table in ${ITEM}
do
		mysql --user=root --password=123456 ${DATABASE_FILTER} < ./filter_tables/${table}.sql
		mysql --user=root --password=123456 ${DATABASE_FILTER} < ./filter_tables/${table}_cache.sql
done

# execute ./build_database_classify/filter.py
# build filter database's tables
python ./build_database_classify/filter.py



# create classify database
python ./build_database_classify/init_classify.py

# import ./classify_tables/*.sql files to classify database
# create classify database's tables
DATABASE_CLASSIFY=classify
for table in disease_info complication user_info
do
		mysql --user=root --password=123456 ${DATABASE_CLASSIFY} < ./classify_tables/${table}.sql
done

# execute ./build_database_classify/classify.py
# build classify database's tables
python ./build_database_classify/classify.py



# recommend system algorithm
python ./build_database_classify/recommend.py
