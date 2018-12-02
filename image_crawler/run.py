"""
@Author: Sun Suibin
@Date: 2018-11-25 19:11:04
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-11-25 19:11:04
"""

import import_helper
import logging
import os
import json
import multiprocessing as mp
# from icrawler.builtin import BingImageCrawler
from config import ENTITY_DIR, DATA_DIR, IMAGE_DIR, ROOT_DIR
# from image_crawler import PrefixImageDownloader


def crawl_book(book, tag, add):
    num = book.split('.')[0]
    title = tag[num]['title']
    entities = json.load(open(os.path.join(ENTITY_DIR, book), 'r'))
    crawled = set()
    for cpt in entities:
        for entity in entities[cpt]['cpt_key']:
            entity = entity[0]
            outpath = os.path.join(IMAGE_DIR, num, entity)
            if entity not in crawled and not os.path.exists(outpath) or add and len(os.listdir(outpath)) == 0:

                cmd = os.popen(
                    f'python {os.path.join(ROOT_DIR,"image_crawler","bbid.py")} -s "illustration {entity} {title}" -o "{outpath}" --limit 4')
                print(cmd.read())
                cmd.close()
                # print(f'book {num}, entity \'{entity}\' crawled.')
                # break
            else:
                print(f'{entity} passed.')
                continue
        # break
    print(f'=====================book {num}, \'{title}\' finished.=======================')


def crawl():
    os.chdir(ROOT_DIR)
    tag = json.load(open(os.path.join(DATA_DIR, 'tag_filtered.json'), 'r'))
    books = os.listdir(ENTITY_DIR)
    with mp.Pool(processes=4) as pool:
        for book in books:
            pool.apply_async(crawl_book, args=(book, tag, True))
        pool.close()
        pool.join()


if __name__ == '__main__':
    crawl()
