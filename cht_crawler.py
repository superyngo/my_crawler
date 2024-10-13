import importlib
import data.source_contracts
import data.source_items
import data.source_MSG_Reports
from modules.crawlers_defs import * 

CsCHTCrawler = cs_factory(dic_cs_cht_crawler_config)
cht_crawler = CsCHTCrawler('EPIS_contract_info_items')
cht_crawler.EPIS_contract_info_items_handler(data.source_contracts.lst_source_contracts)
