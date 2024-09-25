# 20240924
from modules.crawlers_defs import *
from data.source_contracts import lst_source_contracts
multi_driver_crawler = None
# lst_source_contracts = ["23S13A0041","23R13A0051"]
source = lst_source_contracts
task = 'EPIS_contract_batch'

def main():
    global multi_driver_crawler
    fn_log(f"Total contracts count : {len(source)}")
    
    # Start driver
    if multi_driver_crawler:
        multi_driver_crawler._load_instances_components(task)
    else:
        multi_driver_crawler = CsMultiCrawlersManager(task)
        multi_driver_crawler._call_instances('login_cht')()
    
    # EPIS_contract_batch
    multi_driver_crawler.EPIS_contract_batch_handler(source = source)

if __name__ == "__main__":
    main()


