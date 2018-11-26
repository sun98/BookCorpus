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
from icrawler.builtin import BingImageCrawler
from config import ENTITY_DIR, DATA_DIR, IMAGE_DIR, ROOT_DIR
# from image_crawler import PrefixImageDownloader


def crawl():
    os.chdir(ROOT_DIR)
    tag = json.load(open(os.path.join(DATA_DIR, 'tag_filtered.json'), 'r'))
    books = os.listdir(ENTITY_DIR)
    for book in books:
        num = book.split('.')[0]
        title = tag[num]['title']
        entities = json.load(open(os.path.join(ENTITY_DIR, book), 'r'))
        crawled = set()
        for cpt in entities:
            for entity in entities[cpt]['cpt_key']:
                if entity not in crawled:
                    outpath = os.path.join(IMAGE_DIR, num, entity)
                    cmd = os.popen(f'python {os.path.join(ROOT_DIR,"image_crawler","bbid.py")} -s "{entity} in {title}" -o "{outpath}" --limit 4')
                    print(cmd.read())
                    cmd.close()
                    print(f'book {num}, entity \'{entity}\' crawled.')
        break
        print(f'===================book {num}, \'{title}\' finished.=======================')


if __name__ == '__main__':
    crawl()
