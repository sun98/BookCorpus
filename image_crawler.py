"""
@Author: Sun Suibin
@Date: 2018-11-12 21:33:08
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-11-12 21:33:08
"""

from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'images'})
google_crawler.crawl(keyword='dodo', max_num=100, min_size=(200, 200))
