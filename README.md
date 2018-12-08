# Book Corpus

## chapter slicer

## entity analyzer

## image crawler

## mysql app

# Initializing scripts of MySQL:
- Edit the database `host`, `user`, `password` in `./app/db_config.py`

- Create schema `bookcorpus2` in MySQL databases. In MySQL command line, run:

  `mysql> source ./app/db_create_2.sql`
- Insert data int databases. In system command line, run:
  
  `$ python3 -u "./app/db.py"`

- If there is import issue in running python files, please check current working directory.