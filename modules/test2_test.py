from modules.test2 import * 
import importlib
from modules.crawlers_defs import *
import data.source_contracts
import data.source_items
import data.source_MSG_Reports

# test
# lst_source_contracts = ["23S13A0041","23R13A0051"]
# lst_items = ["02502735","21190613"]
# lst_source_MSG_reports = [{'name' : 'RS4212RA4L','postfix' : '50502'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 

multi_driver_crawler = CsMultiCrawlersManager('google')

task = None
while task != "stop":
  if task:multi_driver_crawler.crawling_main(**configs[task])
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


multi_driver_crawler._call_instances('close')()
fn_log("All jobs done!!")



from modules.test2 import * 

CsComposedLoadableDrive = cs_factory(dic_cs_cht_crawler)
cht_drive = CsComposedLoadableDrive('google')
cht_drive.remove_components('google')
cht_drive.get('https://yahoo.com')
cht_drive.load_components('google')
cht_drive2 = CsComposedLoadableDrive('google')
cht_drive.close()
cht_drive2.close()

from modules.test2 import * 
CsMultiChtCrawler = cs_factory(dic_cs_cht_multi_manager)
cht_multi_crawler = CsMultiChtCrawler()
cht_multi_crawler.remove_instances_components('google')
cht_multi_crawler.load_instances_components('google')
cht_multi_crawler.google_handler()
cht_multi_crawler.google_handler(threads=2)
cht_multi_crawler.google_handler(threads=1)
cht_multi_crawler.google_handler(threads=0)
cht_multi_crawler.load_instances_components('google',threads=3)
cht_multi_crawler.threads=0
cht_multi_crawler.crawling_main(task='google', source=[], threads=3)
