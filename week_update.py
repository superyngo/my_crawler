# 20240920
from modules.crawlers_defs import *
from data.source_MSG_Reports import lst_source_MSG_reports
multi_driver_crawler = None 

def main():
    global multi_driver_crawler
    # Start driver
    multi_driver_crawler = CsMultiCrawlersManager('MSG', 'MASIS_InvQry')
    multi_driver_crawler._call_instances('login_cht')()
    
    # MSG 
    lst_test_reports = [{'name' : 'RS4183MA4L'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 
    multi_driver_crawler.MSG_handler(source=lst_source_MSG_reports)

    # MASIS_InvQry
    source = ['50502', '50503', '59511', '59512', '59521', '59531']
    multi_driver_crawler.MASIS_InvQry_handler(source=source)

if __name__ == "__main__":
    main()



