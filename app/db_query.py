"""
@Author: Sun Suibin
@Date: 2018-12-04 19:19:32
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-04 19:19:32
"""

# import import_helper
import pymysql
from app.db_config import DB_HOST, DB_NAME, DB_PW, DB_USER


def query_book_by_name_title(name, author):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME)
    cursor = db.cursor()
    sql_cmd = "select * from book where title like %s or author like %s;"
    cursor.execute(sql_cmd, (f'%{name}%', f'%{author}%'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_title_cptnum(title, cpt_num):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME)
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where image_id in (
        select image_id from image_cpt
        where book_id in (
            select book_id from book
            where title like %s
        )
        and cpt_num=%s
    )"""
    cursor.execute(sql_cmd, (f'%{title}%', cpt_num))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_bookid_cpt_num(book_id, cpt_num):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME)
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where image_id in (
        select image_id from image_cpt
        where book_id=%s and cpt_num=%s
    )"""
    cursor.execute(sql_cmd, (book_id, cpt_num))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_word(word):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME)
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where ent_name like %s"""
    cursor.execute(sql_cmd, (f'%{word}%'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


if __name__ == '__main__':
    # print(query_book_by_name_title('alice', 'carroll')[0])
    # print(query_image_by_title_cptnum('adventures', 3)[0])
    # print(query_image_by_bookid_cpt_num(10002, 3)[0])
    print(query_image_by_word('dodo')[0])
