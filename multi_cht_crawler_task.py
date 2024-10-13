import importlib
import data.source_contracts
import data.source_items
import data.source_MSG_Reports
from modules.crawlers_defs import * 

CsMultiCHTCrawler = cs_factory(dic_cs_cht_multi_crawler_config)
cht_multi_crawler = CsMultiCHTCrawler()

handle_stop = False
while not handle_stop:
  importlib.reload(data.source_contracts)
  importlib.reload(data.source_items)
  importlib.reload(data.source_MSG_Reports)
  from data.source_contracts import lst_source_contracts
  from data.source_items import lst_items
  from data.source_MSG_Reports import lst_source_MSG_reports
  # test
  # lst_source_contracts = ["23S13A0041","23R13A0051"]
  # lst_items = ["02502735","21190613"]
  # lst_source_MSG_reports = [{'name' : 'RS4212RA4L','postfix' : '50502'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 
  configs = {
      'EPIS_contract_batch' : {
        'source' : lst_source_contracts,
        'task' : 'EPIS_contract_batch',
        'threads' : 2
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
        'threads' : 2
    }}
  tasks = ast.literal_eval('["' + input(f"tasks:\n {"\n ".join(configs.keys())}\nor stop:").replace(',', '","') + '"]')
  # config = tasks['config'] if 'config' in 
  for task in tasks:
    if task == 'stop': 
      handle_stop = True
      break
    if task:cht_multi_crawler.crawling_main(**configs[task])


cht_multi_crawler.threads = 0
fn_log("All jobs done!!")

