"""
@Author: Sun Suibin
@Date: 2018-12-04 19:19:32
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-04 19:19:32
"""

# import import_helper
import pymysql
from app.db_config import DB_HOST, DB_NAME, DB_PW, DB_USER


def query_book_by_name_title(name, author, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = "select * from book where title like %s or author like %s;"
        cursor.execute(sql_cmd, (f'%{name}%', f'%{author}%'))
    else:
        sql_cmd = "select * from book where match(title) against (%s) or match(author) against (%s);"
        cursor.execute(sql_cmd, (f'{name}', f'{author}'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_title_cptnum(title, cpt_num, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where title like %s
        ) and cpt_num=%s"""
        cursor.execute(sql_cmd, (f'%{title}%', cpt_num))
    else:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where match(title) against (%s)
        ) and cpt_num=%s"""
        cursor.execute(sql_cmd, (f'{title}', cpt_num))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_bookid_cpt_num(book_id, cpt_num, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where book_id=%s and cpt_num=%s"""
    cursor.execute(sql_cmd, (book_id, cpt_num))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_word(word, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where ent_name like %s"""
    cursor.execute(sql_cmd, (f'%{word}%'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_title_word(title, word, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = """
        select * from image
        where ent_name like %s and book_id in (
            select book_id from book
            where title like %s
        )"""
        cursor.execute(sql_cmd, (f'%{word}%', f'%{title}%'))
    else:
        sql_cmd = """
        select * from image
        where ent_name like %s and book_id in (
            select book_id from book
            where match(title) against (%s)
        )"""
        cursor.execute(sql_cmd, (f'%{word}%', f'{title}'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def query_image_by_title_cpttitle(title, cpt_title, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where title like %s
        ) and cpt_num in (
            select cpt_num from chapter
            where cpt_title like %s
        )"""
        cursor.execute(sql_cmd, (f'%{title}%', f'%{cpt_title}%'))
    else:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where match(title) against (%s)
        ) and cpt_num in (
            select cpt_num from chapter
            where match(cpt_title) against (%s)
        )"""
        cursor.execute(sql_cmd, (f'{title}', f'{cpt_title}'))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


if __name__ == '__main__':
    print(len(query_book_by_name_title('alice', 'carroll', 1)))
    print(len(query_book_by_name_title('alice', 'carroll', 2)))

    print(len(query_image_by_title_cptnum('adventures', 3, 1)))
    print(len(query_image_by_title_cptnum('adventures', 3, 2)))

    print(len(query_image_by_bookid_cpt_num(10002, 3, 1)))
    print(len(query_image_by_bookid_cpt_num(10002, 3, 2)))

    print(len(query_image_by_word('dodo', 1)[0]))
    print(len(query_image_by_word('dodo', 2)[0]))

    print(len(query_image_by_title_cpttitle('alice', 'hole', 1)))
    print(len(query_image_by_title_cpttitle('alice', 'hole', 2)))
