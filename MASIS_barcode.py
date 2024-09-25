# 20240923
from modules.crawlers_defs import *

# Query Barcode by Contract ID and Lot No
source = {"23B12A2491":["1","2",3,4,5]}
task = 'MASIS_barcode'

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




