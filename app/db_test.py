"""
@Author: Sun Suibin
@Date: 2018-12-05 14:58:16
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-05 14:58:16
"""

import pymysql
import time
from app.db_config import DB_HOST, DB_USER, DB_PW, DB_NAME


def get_title_list(db, cursor):
    pass


def get_author_list(db, cursor):
    pass


def get_bid_list(db, cursor):
    pass


def get_kw_list(db, cursor):
    pass


def get_cpt_title_list(db, cursor):
    pass


if __name__ == '__main__':
    db = pymysql.connect(DB_HOST, DB_USER, DB_PW, DB_NAME[2])
    cursor = db.cursor()
    titles = get_title_list(db, cursor)
    authors = get_author_list(db, cursor)
