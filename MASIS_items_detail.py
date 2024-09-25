# 20240705
from modules.crawlers_defs import *
from data.source_items import lst_items

source = lst_items
task = 'MASIS_item_detail'

def main():
    global multi_driver_crawler
    fn_log(f"Total contracts count : {len(source)}")
    
    # Start driver
    if multi_driver_crawler:
        multi_driver_crawler._load_instances_components(task)
    else:
        multi_driver_crawler = CsMultiCrawlersManager(task)
        multi_driver_crawler._call_instances('login_cht')()
    
    # MASIS_barcode
    multi_driver_crawler.MASIS_barcode_handler(source=source)

if __name__ == "__main__":
    main()




def main():
    # Start driver
    driver_crawler = CsDriverCrawler('MASIS_item_detail').login_cht()
    # MASIS_item_detail 
    source = ["02502735","21190613"]
    driver_crawler.MASIS_item_detail_handler(source)

if __name__ == "__main__":
    main()