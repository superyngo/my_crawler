# 20240926
from modules.crawlers_defs import *
from data.source_contracts import lst_source_contracts
from data.source_items import lst_items
from data.source_MSG_Reports import lst_source_MSG_reports
multi_driver_crawler = None
# test
lst_source_contracts = ["23S13A0041","23R13A0051"]
lst_items = ["02502735","21190613"]
lst_source_MSG_reports = [{'name' : 'RS4183MA4L'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 

configs = {
  'EPIS_contract_batch' : {
    'source' : lst_source_contracts,
    'task' : 'EPIS_contract_batch',
    'threads' : 1
  },
  'EPIS_contract_info_items':{
    'source' : lst_source_contracts,
    'task' : 'EPIS_contract_info_items',
    'threads' : 2
  },
  'MASIS_barcode' : {
    'source' : {"23B12A2491":["1","2",3,4,5]},
    'task' : 'MASIS_barcode',
    'threads' : 2
  },
  'MASIS_item_detail' : {
    'source' : lst_items,
    'task' : 'MASIS_item_detail',
    'threads' : 2
  },
  'MSG' : {
    'source' : lst_source_MSG_reports,
    'task' : 'MSG',
    'threads' : 1
  },
  'MASIS_InvQry' : {
    'source' : ['50502', '50503', '59511', '59512', '59521', '59531'],
    'task' : 'MASIS_InvQry',
    'threads' : 1
}}
multi_driver_crawler = multi_driver_crawler or CsMultiCrawlersManager('sharepoint')

if __name__ == "__main__":
    multi_driver_crawler.crawling_main(**configs['MSG'])
    multi_driver_crawler._remove_instances_components('MASIS_InvQry')
    multi_driver_crawler.crawling_main(**(configs['MASIS_InvQry'] | {'threads':2,'source' : ['50502', '50503']}))
    multi_driver_crawler._remove_instances_components('MASIS_InvQry')
    multi_driver_crawler.crawling_main(**(configs['MASIS_InvQry'] | {'source' : ['50502', '50503']}))
    multi_driver_crawler.crawling_main(**configs['EPIS_contract_batch'])
    multi_driver_crawler.crawling_main(**configs['EPIS_contract_info_items'])
    multi_driver_crawler.crawling_main(**configs['MASIS_barcode'])
    multi_driver_crawler.crawling_main(**configs['MASIS_item_detail'])
