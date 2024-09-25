# 20240705
from modules.crawlers_defs import *
from data.source_items import source

def main():
    # Start driver
    driver_crawler = CsDriverCrawler('MASIS_item_detail').login_cht()
    # MASIS_item_detail 
    source = ["02502735","21190613"]
    driver_crawler.MASIS_item_detail_handler(source)

if __name__ == "__main__":
    main()