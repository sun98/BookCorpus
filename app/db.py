"""
Author: Sun Suibin
Date: 2018-12-02 18:31:46
Last Modified by:   Sun Suibin
Last Modified time: 2018-12-02 18:31:46
"""

import json
import os
from datetime import datetime

import pymysql

import import_helper
from config import BOOK_DIR, DATA_DIR
from db_config import DB_HOST, DB_NAME, DB_PW, DB_USER


def insert_book(db, cursor):
    tag_file = os.path.join(DATA_DIR, 'tag_filtered.json')
    tags = json.load(open(tag_file, 'r'))
    try:
        for book in tags:
            info = tags[book]
            author = info['author']
            title = info['title']
            bid = int(info['ebookNo'])
            lang = info['language']
            da = info['releaseDate'].replace('Jan', 'January').replace('Feb', 'February').replace('Mar', 'March').replace('Apr', 'April').replace('Jun', 'June').replace(
                'Jul', 'July').replace('Aug', 'August').replace('Sep', 'September').replace('Oct', 'October').replace('Nov', 'November').replace('Dec', 'December')
            rd = datetime.strftime(datetime.strptime(da, "%B %d, %Y"), "%Y-%m-%d")
            subject = info['subject']
            cr = info['copyrightStatus']
            price = float(info['price'].replace('$', ''))
            cursor.execute('insert into book(book_id,title,author,subject,language,release_date,price,copyright) values(%s,%s,%s,%s,%s,%s,%s,%s)',
                           (bid, title, author, subject, lang, rd, price, cr))
        db.commit()
    except Exception as e:
        print('Exception occured, DB will rollback')
        print(info)
        raise e
        db.rollback()


def insert_data():
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME)
    cursor = db.cursor()
    insert_book(db, cursor)

    db.close()


if __name__ == '__main__':
    insert_data()
