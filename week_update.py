# 20240920
from modules.crawlers_defs import *
from data.source_MSG_Reports import lst_source_MSG_reports

def main():
    # Start driver
    driver_crawler = CsDriverCrawler('MSG', 'MASIS_InvQry').login_cht()
    # MSG 
    lst_test_reports = [{'name' : 'RS4183MA4L'}] # {'name' : 'RS5203A' , 'prefix' : '20240110'} 
    driver_crawler.MSG_handler(source=lst_source_MSG_reports)
    # MASIS_InvQry
    source = ['50502', '50503', '59511', '59512', '59521', '59531']
    driver_crawler.MASIS_InvQry_handler(source=source)

if __name__ == "__main__":
    main()



