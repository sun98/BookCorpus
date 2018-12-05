import numpy as np
"""
@Author: Sun Suibin
@Date: 2018-12-05 14:58:16
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-05 14:58:16
"""

import random
import time

import pymysql

import import_helper
from app.db_config import DB_HOST, DB_NAME, DB_PW, DB_USER
from app.db_query import *


MAX_N = 10


def get_title_list(db, cursor):
    cursor.execute('select title from book order by rand() limit %s', (MAX_N))
    titles = [x[0] for x in cursor.fetchall()]
    for i in range(len(titles)):
        if i < int(2/5*MAX_N):
            titles[i] = ' '.join(titles[i].strip().split(' ')[random.randint(0, len(titles[i].strip().split(' ')) - 1)])
        elif i < int(4/5*MAX_N):
            titles[i] = ' '.join(titles[i].strip().split(' ')[random.randint(0, len(titles[i].strip().split(' ')) - 1):
                                                              random.randint(0, len(titles[i].strip().split(' ')) - 1) + 2])
        elif i < int(4.5/5*MAX_N):
            titles[i] = ' '.join(titles[i].strip().split(' ')[random.randint(0, int(len(titles[i].strip().split(' ')) / 2 - 1))                                                              : random.randint(int(len(titles[i].strip().split(' ')) / 2), len(titles[i].strip().split(' ')) - 1)])
    return titles


def get_author_list(db, cursor):
    cursor.execute('select author from book order by rand() limit %s', (MAX_N))
    authors = [x[0] for x in cursor.fetchall()]
    for i in range(len(titles)):
        if i < int(2/5*MAX_N):
            authors[i] = ' '.join(authors[i].strip().split(' ')[random.randint(0, len(authors[i].strip().split(' ')) - 1)])
    return authors


def get_bid_list(db, cursor):
    cursor.execute('select book_id from book order by rand() limit %s', (MAX_N))
    bids = [x[0] for x in cursor.fetchall()]
    return bids


def get_kw_list(db, cursor):
    cursor.execute('select ent_name from entity order by rand() limit %s', (MAX_N))
    kws = [x[0] for x in cursor.fetchall()]
    return kws


def get_cpt_title_list(db, cursor):
    cursor.execute('select cpt_title from chapter order by rand() limit %s', (MAX_N))
    cpt_titles = [x[0] for x in cursor.fetchall()]

    for i in range(len(cpt_titles)):
        if i < int(2/5*MAX_N):
            cpt_titles[i] = ' '.join(cpt_titles[i].strip().split(' ')[random.randint(0, len(cpt_titles[i].strip().split(' ')) - 1)])
        elif i < int(4/5*MAX_N):
            cpt_titles[i] = ' '.join(cpt_titles[i].strip().split(' ')[random.randint(0, len(cpt_titles[i].strip().split(' ')) - 1):
                                                                      random.randint(0, len(cpt_titles[i].strip().split(' ')) - 1) + 2])
        elif i < int(4.5/5*MAX_N):
            cpt_titles[i] = ' '.join(cpt_titles[i].strip().split(' ')[random.randint(0, int(len(cpt_titles[i].strip().split(' ')) / 2 - 1))                                                                      : random.randint(int(len(cpt_titles[i].strip().split(' ')) / 2), len(cpt_titles[i].strip().split(' ')) - 1)])
    return cpt_titles


def real_test(titles, authors, bids, kws, cptts):
    record = [[[] for _ in range(5)] for __ in range(2)]
    length = [[[] for _ in range(5)] for __ in range(2)]
    print('test for real queries:')
    for ver in [1, 2]:
        print(f'start test for version {ver}')
        for title in titles:
            for author in authors:
                res, cost = query_book_by_name_author(title, author, ver)
                length[ver-1][0].append(len(res))
                record[ver-1][0].append(cost)
            for cptt in cptts:
                res, cost = query_image_by_title_cpttitle(title, cptt, ver)
                length[ver-1][1].append(len(res))
                record[ver-1][1].append(cost)
            for kw in kws:
                res, cost = query_image_by_title_word(title, kw, ver)
                length[ver-1][2].append(len(res))
                record[ver-1][2].append(cost)
        print('\tstep A finished')
        # for i in range(3):
        #     print(f'\t\taverage time cost: {np.average(np.array(record[ver-1][i]))}s,\ttotal record: {np.average(np.array(length[ver-1][i]))}')
        for cpt_num in range(MAX_N):
            cpt_num %= 10
            for bid in bids:
                res, cost = query_image_by_bookid_cpt_num(bid, cpt_num, ver)
                length[ver-1][3].append(len(res))
                record[ver-1][3].append(cost)
            for title in titles:
                res, cost = query_image_by_title_cptnum(title, cpt_num, ver)
                length[ver-1][4].append(len(res))
                record[ver-1][4].append(cost)
        print('\tstep B finished')
        # for i in range(3, 5):
        #     print(f'\t\taverage time cost: {np.average(np.array(record[ver-1][i]))}s,\ttotal record: {np.average(np.array(length[ver-1][i]))}')
    record = np.array(record)
    for i in [0, 1]:
        print(f'version {i+1}:')
        for j in range(5):
            print(f'\taverage time cost: {np.average(record[i][j])}s')
        print(f'\n\ttotal time cost: {np.sum(record[i])}s')


def single_test():
    print('test for secodary index')
    for ver in [1, 2]:
        costs, length = [], []
        for i in range(10000):
            n = random.randint(1, 50000)
            res, cost = query_image_by_bookid(n, ver)
            length.append(len(res))
            costs.append(cost)
        print(f'version {ver}:')
        print(f'\taverage time cost: {np.average(costs)}s')
        print(f'\taverage record number: {np.average(length)}')
        print(f'\ttotal time cost:{np.sum(costs)}')


if __name__ == '__main__':
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[1])
    cursor = db.cursor()
    titles = get_title_list(db, cursor)
    authors = get_author_list(db, cursor)
    bids = get_bid_list(db, cursor)
    kws = get_kw_list(db, cursor)
    cptts = get_cpt_title_list(db, cursor)
    cursor.close()
    db.close()

    # print(titles)
    # print(authors)
    # print(bids)
    # print(kws)
    # print(cptts)

    real_test(titles, authors, bids, kws, cptts)
    # single_test()
