import importlib
import data.source_contracts
import data.source_items
import data.source_MSG_Reports
from modules.crawlers_defs import * 

def convert_string_to_dict(input_string):
    result = {}
    current_key = ''
    in_brackets = False
    bracket_content = ''

    for char in input_string:
        if char in '{[':
            in_brackets = True
            bracket_content = char
        elif char in ']}':
            in_brackets = False
            bracket_content += char
            result[current_key.rstrip(':').strip()] = ast.literal_eval(bracket_content)
            current_key = ''
        elif char == ',' and not in_brackets:
            if current_key and current_key.rstrip(':').strip() not in result:
                result[current_key.rstrip(':').strip()] = None
            current_key = ''
        elif in_brackets:
            bracket_content += char
        else:
            current_key += char

    if current_key and current_key.rstrip(':').strip() not in result:
        result[current_key.rstrip(':').strip()] = None

    return result

def main():
  CsCHTCrawler = cs_factory(dic_cs_cht_crawler_config)
  cht_crawler = CsCHTCrawler()

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
        'EPIS_contract_batch' : lst_source_contracts,
        'EPIS_contract_info_items': lst_source_contracts,
        'MASIS_barcode': {"23B12A2491":["1","2",3,4,5]},
        'MASIS_item_detail': lst_items,
        'MSG': lst_source_MSG_reports,
        'MASIS_InvQry': ['50503', '59511', '59512', '59521', '59531']
      }
    tasks = convert_string_to_dict(input(f"tasks:\n {"\n ".join(configs.keys())}\nor stop:"))
    # config = tasks['config'] if 'config' in 
    for task, source in tasks.items():
      if task == 'stop': 
        handle_stop = True
        break
      if task:
        if task not in cht_crawler._loaded_components: cht_crawler.load_components(task)
        getattr(cht_crawler, task + '_handler')(source if source else configs.get(task))
  fn_log("Jobs done!!")
  cht_crawler.close()
  
if __name__ == "__main__":
    main()