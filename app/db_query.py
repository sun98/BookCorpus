"""
@Author: Sun Suibin
@Date: 2018-12-04 19:19:32
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-04 19:19:32
"""

import string
import time

import pymysql

import import_helper
from app.db_config import DB_HOST, DB_NAME, DB_PW, DB_USER


def query_book_by_name_author(title, author, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        titles = title.strip().split(' ')
        authors = author.strip().split(' ')
        sql_cmd = "select * from book where title like %s "
        for t in titles[1:]:
            sql_cmd += "or title like %s "
        for a in authors:
            sql_cmd += "or author like %s "
        titles = tuple(f'%{x}%' for x in titles)
        authors = tuple(f'%{x}%' for x in authors)
        old = time.time()
        cursor.execute(sql_cmd, titles + authors)
        total = time.time() - old
    else:
        sql_cmd = "select * from book where match(title) against (%s) or match(author) against (%s);"
        old = time.time()
        cursor.execute(sql_cmd, (f'{title}', f'{author}'))
        total = time.time() - old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_title_cptnum(title, cpt_num, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        titles = title.strip().split(' ')
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where title like %s """
        for t in titles[1:]:
            sql_cmd += 'or title like %s'
        sql_cmd += """) and cpt_num=%s;"""
        texts = tuple(f'%{x}%' for x in titles)
        old = time.time()
        cursor.execute(sql_cmd, texts + (cpt_num,))
        total = time.time() - old
    else:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where match(title) against (%s)
        ) and cpt_num=%s"""
        old = time.time()
        cursor.execute(sql_cmd, (f'{title}', cpt_num))
        total = time.time()-old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_bookid_cpt_num(book_id, cpt_num, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where book_id=%s and cpt_num=%s"""
    old = time.time()
    cursor.execute(sql_cmd, (book_id, cpt_num))
    total = time.time()-old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_word(word, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    words = word.strip().split(' ')
    sql_cmd = """
    select * from image
    where ent_name like %s """
    for w in words[1:]:
        sql_cmd += 'ent_name like %s '
    texts = tuple(f'%{x}%' for x in words)
    old = time.time()
    cursor.execute(sql_cmd, texts)
    total = time.time() - old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_title_word(title, word, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = """
        select * from image
        where ent_name like %s and book_id in (
            select book_id from book
            where title like %s """
        for t in title.strip().split(' ')[1:]:
            sql_cmd += 'or title like %s '
        sql_cmd += ')'
        texts = tuple(f'%{x}%' for x in title.strip().split(' '))
        old = time.time()
        cursor.execute(sql_cmd, (f'%{word}%',) + texts)
        total = time.time()-old
    else:
        sql_cmd = """
        select * from image
        where ent_name like %s and book_id in (
            select book_id from book
            where match(title) against (%s)
        )"""
        old = time.time()
        cursor.execute(sql_cmd, (f'%{word}%', f'{title}'))
        total = time.time()-old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_title_cpttitle(title, cpt_title, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    if ver == 1:
        sql_cmd = """
        select * from image
        where book_id in (
            select book_id from book
            where title like %s """
        for t in title.strip().split(' ')[1:]:
            sql_cmd += 'or title like %s '
        sql_cmd += """
        ) and cpt_num in (
            select cpt_num from chapter
            where cpt_title like %s"""
        for ct in cpt_title.strip().split(' ')[1:]:
            sql_cmd += 'or cpt_title like %s'
        sql_cmd += """
        )"""
        titletexts = tuple(f'%{x}%' for x in title.strip().split(' '))
        cttexts = tuple(f'%{x}%' for x in cpt_title.strip().split(' '))
        old = time.time()
        cursor.execute(sql_cmd, titletexts + cttexts)
        total = time.time()-old
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
        old = time.time()
        cursor.execute(sql_cmd, (f'{title}', f'{cpt_title}'))
        total = time.time()-old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


def query_image_by_bookid(book_id, ver=2):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[ver])
    cursor = db.cursor()
    sql_cmd = """
    select * from image
    where book_id=%s"""
    old = time.time()
    cursor.execute(sql_cmd, (book_id, ))
    total = time.time()-old
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows, total


if __name__ == '__main__':
    print(len(query_book_by_name_author('alice', 'carroll', 1)[0]))
    print(len(query_book_by_name_author('alice', 'carroll', 2)[0]))

    print(len(query_image_by_title_cptnum('adventures', 3, 1)[0]))
    print(len(query_image_by_title_cptnum('adventures', 3, 2)[0]))

    print(len(query_image_by_bookid_cpt_num(10002, 3, 1)[0]))
    print(len(query_image_by_bookid_cpt_num(10002, 3, 2)[0]))

    print(len(query_image_by_word('dodo', 1)[0]))
    print(len(query_image_by_word('dodo', 2)[0]))

    print(len(query_image_by_title_word('alice adventure', 'dodo', 1)[0]))
    print(len(query_image_by_title_word('alice adventure', 'dodo', 2)[0]))

    print(len(query_image_by_title_cpttitle('alice', 'hole', 1)[0]))
    print(len(query_image_by_title_cpttitle('alice', 'hole', 2)[0]))
