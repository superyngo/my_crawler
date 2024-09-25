# 20240920
# fetch contracts info, items, types
from modules.crawlers_defs import *
from data.source_contracts import lst_source_contracts
import pdb
# lst_source_contracts = ["23S13A0041","23R13A0051"]

dic_splitted_drivers = {}
int_threads = 2
fn_log(f"Total contracts count : {len(lst_source_contracts)}")

def wrapper_contracts(index:int, source:list[str]):
    global dic_splitted_drivers
    # init driver and connect to masis
    if index in dic_splitted_drivers:
        driver_crawler = dic_splitted_drivers[index].driver
        dic_splitted_drivers[index].data = source
    else:
        dic_splitted_drivers[index] = CsSplittedDrivers(driver = CsDriverCrawler('EPIS_contract_info_items').login_cht(), data = source)
        driver_crawler = dic_splitted_drivers[index].driver
    driver_crawler.EPIS_contract_info_items_handler(source = source, index = index)
def main():
    multithreading(lst_source_contracts, wrapper_contracts, int_threads)
    fn_log('Contracts Info and Items saved!!')
    # pdb.set_trace()

if __name__ == "__main__":
    main()