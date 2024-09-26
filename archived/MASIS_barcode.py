# 20240926
from data.configs import *

if __name__ == "__main__":
    multi_driver_crawler = multi_driver_crawler or CsMultiCrawlersManager()
    multi_driver_crawler.crawling_main(**configs['MASIS_barcode'])






