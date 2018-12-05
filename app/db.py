"""
@Author: Sun Suibin
@Date: 2018-12-02 18:31:46
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-02 18:31:46
"""

import json
import os
import unicodedata
from datetime import datetime

import pymysql

import import_helper
from config import APP_DIR, BOOK_DIR, DATA_DIR, IMAGE_DIR
from db_config import DB_HOST, DB_NAME, DB_PW, DB_USER


def unicode(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def reset_db(db, cursor):
    try:
        cursor.execute('source %s', os.path.join(APP_DIR, 'reset_database.sql'))
        db.commit()
        print('db reset')
    except Exception as e:
        db.rollback()
        print('Exception occured, DB will rollback')
        raise e


def insert_book(db, cursor):
    tag_file = os.path.join(DATA_DIR, 'tag_filtered.json')
    tags = json.load(open(tag_file, 'r'))
    try:
        count = 1
        print()
        for book in tags:
            print(f'\rinsert book {str(count).ljust(6)}/{len(tags)}', end='')
            count += 1
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
            burl = os.path.join(BOOK_DIR, f'f{book}.html')
            cursor.execute('insert into book(book_id,title,author,subject,language,release_date,price,copyright,burl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (bid, title, author, subject, lang, rd, price, cr, burl))
        db.commit()
    except Exception as e:
        print('Exception occured in "insert book", DB will rollback')
        print(info)
        db.rollback()
        raise e


def insert_chapter(db, cursor):
    cpt_path = os.path.join(DATA_DIR, 'chapters')
    books = os.listdir(cpt_path)
    try:
        count = 1
        print()
        for book in books:
            print(f'\rinsert chapter {str(count).ljust(6)}/{len(books)}', end='')
            count += 1
            book_path = os.path.join(cpt_path, book)
            cpts = json.load(open(book_path, 'r'))
            bid = int(book.split('.')[0])
            for cpt in cpts:
                cpt_num = int(cpt) + 1
                cpt_title = cpts[cpt]['cpt_name']
                cursor.execute('insert into chapter(book_id,cpt_num,cpt_title) values(%s,%s,%s)', (bid, cpt_num, cpt_title))
        db.commit()
    except Exception as e:
        print('Exception occured in "insert chapter", DB will rollback')
        print(book, cpt_title)
        db.rollback()
        raise e


def insert_entity(db, cursor):
    ent_path = os.path.join(DATA_DIR, 'entities')
    books = os.listdir(ent_path)
    try:
        count = 1
        print()
        for book in books:
            print(f'\rinsert entity {str(count).ljust(6)}/{len(books)}', end='')
            count += 1
            book_path = os.path.join(ent_path, book)
            entities = json.load(open(book_path, 'r'))
            bid = int(book.split('.')[0])
            for cpt in entities:
                ent_set = set()
                ents = entities[cpt]['cpt_key']
                cpt_num = int(entities[cpt]['key_name'])+1
                for ent in ents:
                    ent_name = unicode(ent[0].replace('\u017f', 's').replace('\u00e6', 'ae')).lower()
                    ent_set.add(ent_name)
                for ent in ent_set:
                    try:
                        cursor.execute('insert into entity(book_id,ent_name,cpt_num) values(%s,%s,%s)', (bid, ent, cpt_num))
                    except pymysql.err.IntegrityError:
                        pass
        db.commit()
    except Exception as e:
        print('Exception occured in "insert entity", DB will rollback')
        print(book, ent)
        db.rollback()
        raise e


def insert_cpt_ent(db, cursor):
    ent_path = os.path.join(DATA_DIR, 'entities')
    books = os.listdir(ent_path)
    try:
        count = 1
        print()
        for book in books:
            print(f'\rinsert cpt_ent {str(count).ljust(6)}/{len(books)}', end='')
            count += 1
            book_path = os.path.join(ent_path, book)
            entities = json.load(open(book_path, 'r'))
            bid = int(book.split('.')[0])
            for cpt in entities:
                ent_set = set()
                ents = entities[cpt]['cpt_key']
                for ent in ents:
                    ent_name = unicode(ent[0].replace('\u017f', 's').replace('\u00e6', 'ae')).lower()
                    ent_set.add(ent_name)
                for ent_name in ent_set:
                    cursor.execute('insert into cpt_ent(book_id,cpt_num,ent_name) values(%s,%s,%s)', (bid, int(cpt), ent_name))
        db.commit()
    except Exception as e:
        print('Exception occured in "insert cpt_ent", DB will rollback')
        print(book, ent)
        db.rollback()
        raise e


def insert_image(db, cursor):
    # img_path = os.path.join(DATA_DIR, 'images')
    # books = os.listdir(img_path)
    # try:
    #     count = 1
    #     print()
    #     for book in books:
    #         print(f'\rinsert image {str(count).ljust(6)}/{len(books)}', end='')
    #         count += 1
    #         book_path = os.path.join(img_path, book)
    #         try:
    #             entities = os.listdir(book_path)
    #         except NotADirectoryError:
    #             continue
    #         bid = int(book)
    #         for entity in entities:
    #             ent_path = os.path.join(book_path, entity)
    #             for img in os.listdir(ent_path):
    #                 cursor.execute('insert into image(image_id,book_id,ent_name,iurl) values(%s,%s,%s,%s)',
    #                                (None, bid, entity, os.path.join(ent_path, img)))
    #     db.commit()
    # except Exception as e:
    #     print('Exception occured in "insert image", DB will rollback')
    #     print(book, entity)
    #     db.rollback()
    #     raise e
    ent_path = os.path.join(DATA_DIR, 'entities')
    books = os.listdir(ent_path)
    try:
        count = 1
        print()
        for book in books:
            print(f'\rinsert image {str(count).ljust(6)}/{len(books)}', end='')
            count += 1
            book_path = os.path.join(ent_path, book)
            entities = json.load(open(book_path, 'r'))
            bid = int(book.split('.')[0])
            for cpt in entities:
                ent_set = set()
                ents = entities[cpt]['cpt_key']
                cpt_num = int(entities[cpt]['key_name']) + 1
                for ent in ents:
                    ent_name = unicode(ent[0].replace('\u017f', 's').replace('\u00e6', 'ae')).lower()
                    ent_set.add(ent_name)
                for ent in ent_set:
                    img_folder = os.path.join(IMAGE_DIR, str(bid), ent)
                    if not os.path.exists(img_folder):
                        continue
                    for img in os.listdir(img_folder):
                        cursor.execute('insert into image(image_id,book_id,ent_name,cpt_num,iurl) values(%s,%s,%s,%s,%s)',
                                       (None, bid, ent, cpt_num, os.path.join(img_folder, img)))
        db.commit()
    except Exception as e:
        print('Exception occured in "insert image", DB will rollback')
        print(book, ent)
        db.rollback()
        raise e


def insert_image_cpt(db, cursor):
    sql_cmd = '''insert into image_cpt(image_id,book_id,cpt_num) select image_id,image.book_id,cpt_ent.cpt_num from image natural left join cpt_ent;'''
    try:
        cursor.execute(sql_cmd)
        print('image_cpt inserted')
    except Exception as e:
        print('Exception occured in "insert image_cpt", DB will rollback')
        db.rollback()
        raise e


def insert_all():
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[1])
    cursor = db.cursor()

    # insert_book(db, cursor)
    # insert_chapter(db, cursor)
    # insert_entity(db, cursor)
    # insert_cpt_ent(db, cursor)
    insert_image(db, cursor)
    # insert_image_cpt(db, cursor)    # may not work

    cursor.close()
    db.close()


if __name__ == '__main__':
    insert_all()
