"""
@Author: Sun Suibin
@Date: 2018-11-25 19:11:04
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-11-25 19:11:04
"""

import json
import logging
import multiprocessing as mp
import os

import import_helper
from icrawler.builtin import BingImageCrawler
from config import DATA_DIR, ENTITY_DIR, IMAGE_DIR, ROOT_DIR

# from image_crawler import PrefixImageDownloader


def crawl_book(book, tag, add):
    num = book.split('.')[0]
    title = tag[num]['title']
    entities = json.load(open(os.path.join(ENTITY_DIR, book), 'r'))
    crawled = set()
    for cpt in entities:
        for entity in entities[cpt]['cpt_key'][:2]:
            entity = entity[0]
            outpath = os.path.join(IMAGE_DIR, num, entity)
            if entity not in crawled and not os.path.exists(outpath) or add and len(os.listdir(outpath)) == 0:
                title = title.replace('"', '').replace("'", '')
                keyword = f"illustration {entity} {title}"
                # command = f'python {os.path.join(ROOT_DIR,"image_crawler","bbid.py")} -s "illustration {entity} {title}" -o "{outpath}" --limit 4' if not add else f'python {os.path.join(ROOT_DIR,"image_crawler","bbid.py")} -s "{entity} in {title}" -o "{outpath}" --limit 4'
                # cmd = os.popen(command)
                # cmd.read()
                # cmd.close()
                # print(f'book {num}, entity \'{entity}\' crawled.')
                # break
                bing_crawler = BingImageCrawler(storage={'root_dir': outpath})
                bing_crawler.crawl(keyword=keyword, max_num=2)
            else:
                # print(f'{entity} passed.')
                continue
        # break
    print(f'==book {num}, \'{title}\' finished.==')


def crawl(addition):
    os.chdir(ROOT_DIR)
    tag = json.load(open(os.path.join(DATA_DIR, 'tag_filtered.json'), 'r'))
    books = os.listdir(ENTITY_DIR)
    exist_books = os.listdir(IMAGE_DIR)
    if addition:
        print(len(exist_books))
    with mp.Pool(processes=12) as pool:
        for book in books:
            if addition and book.split('.')[0] in exist_books:
                pool.apply_async(crawl_book, args=(book, tag, addition))
            else:
                pool.apply_async(crawl_book, args=(book, tag, addition))
        pool.close()
        pool.join()


if __name__ == '__main__':
    crawl(True)
