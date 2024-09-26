# 20240924
from data.configs import *

if __name__ == "__main__":
    multi_driver_crawler = multi_driver_crawler or CsMultiCrawlersManager()
    multi_driver_crawler.crawling_main(**configs['EPIS_contract_batch'])


