# 20240926
import importlib
from modules.crawlers_defs import *
import data.source_contracts
import data.source_items
import data.source_MSG_Reports

# test
# lst_source_contracts = ["23S13A0041","23R13A0051"]
# lst_items = ["02502735","21190613"]
# lst_source_MSG_reports = [{'name' : 'RS4212RA4L','postfix' : '50502'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 

multi_driver_crawler = CsMultiCrawlersManager()

task = None
while task != "stop":
  importlib.reload(data.source_contracts)
  importlib.reload(data.source_items)
  importlib.reload(data.source_MSG_Reports)
  from data.source_contracts import lst_source_contracts
  from data.source_items import lst_items
  from data.source_MSG_Reports import lst_source_MSG_reports


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
      'threads' : 1
    },
    'MSG' : {
      'source' : lst_source_MSG_reports,
      'task' : 'MSG',
      'threads' : 1
    },
    'MASIS_InvQry' : {
      'source' : ['50503', '59511', '59512', '59521', '59531'],
      'task' : 'MASIS_InvQry',
      'threads' : 1
  }}

  task = input(f"tasks:\n {"\n ".join(configs.keys())}\nor stop:")
  multi_driver_crawler.crawling_main(**configs[task])

multi_driver_crawler._call_instances('close')()
fn_log("All jobs done!!")