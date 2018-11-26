"""
@Author: Sun Suibin
@Date: 2018-11-12 21:59:44
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-11-12 21:59:44

"""
from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
DATA_DIR = path.join(ROOT_DIR, 'data')

BOOK_DIR = path.join(DATA_DIR, "books")
BOOK_SA_DIR = path.join(DATA_DIR, 'book_samples')
IMAGE_DIR = path.join(DATA_DIR, "images")
CHAPTER_DIR = path.join(DATA_DIR, 'chapters')
ENTITY_DIR = path.join(DATA_DIR, 'entities')
