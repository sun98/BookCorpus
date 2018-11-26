"""
@Author: Sun Suibin
@Date: 2018-11-12 21:33:08
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-11-12 21:33:08
"""

from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from icrawler.utils import Proxy, ProxyPool, ProxyScanner

import import_helper
from config import DATA_DIR, IMAGE_DIR


# class PrefixImageDownloader(ImageDownloader):
#     def __init__(self, prefix='', *args, **kwargs):
#         self.prefix = prefix
#         return super().__init__(*args, **kwargs)

#     def get_filename(self, task, default_ext):
#         return self.prefix + '_' + super().get_filename(task, default_ext)


class MyCrawler(BingImageCrawler):
    #     def set_proxy_pool(self, pool=None):
    #         self.proxy_pool = ProxyPool()
    #         self.proxy_pool.add_proxy(Proxy('127.0.0.1:1080', 'http'))
    #         self.proxy_pool.add_proxy(Proxy('127.0.0.1:1080', 'https'))
    #         return super().set_proxy_pool(pool=pool)
    pass


if __name__ == '__main__':
    # prefix_image_downloader = PrefixImageDownloader()
    google_crawler = MyCrawler(storage={'root_dir': IMAGE_DIR})
    google_crawler.crawl(keyword='dodo in Alice\'s Adventures in Wonderland', max_num=1, min_size=(200, 200))
