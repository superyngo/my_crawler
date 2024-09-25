# 20240815
from modules.crawlers_defs import *
from Python.Crawler.data.source_contracts import lst_source_contracts_items


# Create a lock object
# FOLDER_PATH = f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\contract_detail"
# os.makedirs(FOLDER_PATH, exist_ok=True)
CONTRACT_ITEMS_TABLE_NAME = r'T_Contract_Items'
# Connect to the SQLite database

lst_source_contracts_items = ["MAA10A2941", "23C11A3221"]
int_total = len(lst_source_contracts_items)
int_finished_count = 0
dic_drivers = {}
int_threads = 1
DIC_COLUMNS_NAMES_CONTRACT_ITEMS = {
    12 : ["id, 契約編號, 材料編號, 名稱, 單位, 明細來源, IT類別, 規格, 數量, 單價, 小計, 備註", "一般"],
    13 : ["id, 契約編號, 材料編號, 名稱, 單位, 明細來源, IT類別, 規格, 數量, 單價, 小計, 小計調整, 備註", "一般"],
    15 : ["id, 契約編號, 材料編號, 名稱, 單位, 明細來源, IT類別, 規格, 數量, 幣別, 外幣單價, 單價, 外幣小計, 小計, 備註", "外幣"],
    20 : ["id, 契約編號, 材料編號, 名稱, 單位, 明細來源, IT類別, 規格, 數量, 單價, 小計, 備註, 查型錄, 優惠計算說明, 查證方式, 查證金額, 查證結果, 契約類別, 來源契約編號, 共同供應契約資訊", "共契"]
}

def wrapper_thread(index, source):
    global int_total, int_finished_count, dic_drivers
    # Start driver and connect to masis
    if index in dic_drivers:
        driver_EPIS_contract_items = dic_drivers[index]
    else:
        driver_EPIS_contract_items = dic_drivers[index] = CsEPISContractInfoItems()
    # main
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for contract in source:
        lst_data = []
        with LOCK:
            int_finished_count += 1
        try:
            fn_log(f"Start fetching {contract} items.")
            lst_data = driver_EPIS_contract_items.query_contract_items(contract)
        except UnexpectedAlertPresentException:
            pass
        except TimeoutException:
            fn_log(f"{contract} has no data. {int_finished_count} of {int_total} finished")
            continue
        int_len_of_lst = len(lst_data[0])
        # create table if not exited
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {CONTRACT_ITEMS_TABLE_NAME} (
            id           TEXT     PRIMARY KEY
                                UNIQUE
                                NOT NULL,
            契約編號         TEXT     NOT NULL,
            材料編號         TEXT     NOT NULL,
            名稱           TEXT,
            單位           TEXT,
            明細來源         TEXT,
            IT類別         TEXT,
            規格           TEXT,
            數量           INTEGER,
            幣別           TEXT,
            外幣單價         NUMERIC,
            單價           INTEGER,
            外幣小計         NUMERIC,
            小計           INTEGER,
            備註           TEXT,
            查型錄          TEXT,
            優惠計算說明       TEXT,
            查證方式         TEXT,
            查證金額         INTEGER,
            查證結果         TEXT,
            契約類別         TEXT,
            來源契約編號       TEXT,
            共同供應契約資訊     TEXT,
            last_updated DATETIME NOT NULL
                                DEFAULT (CURRENT_TIMESTAMP) 
        );
        '''
        cursor.execute(create_table_sql)
        # Prepare the SQL query
        insert_replace_sql  = f'''
        INSERT OR REPLACE INTO {CONTRACT_ITEMS_TABLE_NAME} (
            {DIC_COLUMNS_NAMES_CONTRACT_ITEMS[int_len_of_lst][0]}
        ) VALUES ({",".join(["?"] * int_len_of_lst)})
        '''
        # Iterate over the list and execute the query for each record
        with LOCK:
            # Write Types
            cursor.execute(f"INSERT OR REPLACE INTO T_Contract_Type (契約編號, 契約類別) VALUES ('{contract}', '{DIC_COLUMNS_NAMES_CONTRACT_ITEMS[int_len_of_lst][1]}')")
            # DELETE operation
            cursor.execute(f"DELETE FROM {CONTRACT_ITEMS_TABLE_NAME} WHERE 契約編號 = '{contract}'")
            cursor.executemany(insert_replace_sql , lst_data)
            # Commit the changes to the database
            conn.commit()
        
        fn_log(f"{contract} items saved!! {int_finished_count} of {int_total} finished")
    conn.close()
    test = input('Waiting: ')

multithreading(lst_source_contracts_items, wrapper_thread, int_threads)

# Close the connection


