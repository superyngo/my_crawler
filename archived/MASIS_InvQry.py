# 20240912
from modules.crawlers_defs import *


# MASIS_InvQry
MASIS_InvQry_report_name = 'MASIS_InvQry'
source = ['50502', '50503', '59511', '59512', '59521', '59531']
# Start driver and connect to masis
driver_crawler = CsDriverCrawler()
# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
driver_crawler.get(driver_crawler.dic_URLs[MASIS_InvQry_report_name])
# main
for txtWhno in source:        
    fn_log(f"start fetching {txtWhno} inventory")
    dic_query = {'MASIS_InvQry_report_name':MASIS_InvQry_report_name, 'arg':txtWhno}
    # Input contract ID
    lst_data = driver_crawler.query(**dic_query)
    if len(lst_data) == 0:
        fn_log(f"{txtWhno} has no inventory")
        continue
    fn_log(f"{txtWhno} inventory fetched")
    # Prepare the SQL query
    insert_replace_sql = f'''
    INSERT OR REPLACE INTO {MASIS_InvQry_report_name} (
        項次, 庫號, 材料編號, 名稱, 料別, 呆料, 最高庫存, 實際庫存, 可用庫存, 待收數, 待退數, 待調出數, 待撥入數, 待發數, 安全存量, 上月結存數, 上月單價, 累退數, 累調出數, 累撥入數, 累領數, 料位, 管料員
    ) VALUES ({",".join(["?"] * 23)})
    '''
    # DELETE operation
    cursor.execute(f"DELETE FROM {MASIS_InvQry_report_name} WHERE 庫號 = '{txtWhno}'")
    # Iterate over the list and execute the query for each record
    cursor.executemany(insert_replace_sql , lst_data)
    # Commit the changes to the database
    conn.commit()
    fn_log(f"{txtWhno} inventory data saved")
conn.close()
driver_crawler.close()
