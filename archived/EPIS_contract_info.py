# 20240711
from modules.crawlers_defs import *
from Python.Crawler.data.source_contracts import lst_source_contracts_info


# FOLDER_PATH = f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\contract_info"
TABLE_NAME = r'T_Contract_Info'
# os.makedirs(FOLDER_PATH, exist_ok=True)

# test
lst_source_contracts_info = ['23W13A1811']
# source = ['23W13A1811','23W13A1911','MAC04A0031']
# self=csEPISContractInfoItems()
# contract='MA310A4311'

dic_drivers = {}
int_total = len(lst_source_contracts_info)
int_finished_count = 0
int_threads = 1

def wrapper_thread_init_drivers(index, _sublist):
    global dic_drivers
    dic_drivers[index] = CsEPISContractInfoItems()

def wrapper_thread(index, source):
    global int_total, int_finished_count, dic_drivers
    # Start driver and connect to masis
    if index in dic_drivers:
        driver_EPIS_contract_info = dic_drivers[index]
    else:
        driver_EPIS_contract_info = dic_drivers[index] = CsEPISContractInfoItems()
    lst_contracts_info = []
        # main
    for contract in source:
        with LOCK:
            int_finished_count += 1
        try:
            fn_log(f"Start fetching {contract} info.")
            lst_contracts_info += [[contract] + driver_EPIS_contract_info.query_contract_info(contract)]
            fn_log(f"Fetching {contract} info succeed, {int_finished_count} of {int_total} finished!")
        except TimeoutException:
            fn_log(f"{contract} has no data. {int_finished_count} of {int_total} finished")
            continue
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create the table if it doesn't exist
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        契約編號 TEXT PRIMARY KEY UNIQUE NOT NULL,
        契約幣別 TEXT,
        契約金額_外幣 REAL,
        台銀賣出匯率日期 TEXT,
        台銀即期賣出匯率 REAL,
        國際貿易條件 TEXT,
        約定履約日期 TEXT,
        決標資訊 TEXT,
        免收履約保證金 INTEGER,
        履約保證金繳納方式 TEXT,
        履約保證金額 REAL,
        履約保證有效期限 TEXT,
        免收保固保證金 INTEGER,
        保固保證金繳納方式 TEXT,
        保固保證金額 REAL,
        保固保證有效期限 TEXT,
        保固期限 TEXT,
        已全部請款完畢 INTEGER,
        契約是否變更 INTEGER,
        最後契約變更日期 TEXT,
        契約備註 TEXT,
        契約狀態 TEXT,
        last_update DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(create_table_sql)
    # Prepare the SQL query
    insert_replace_sql  = f'''
    INSERT OR REPLACE INTO {TABLE_NAME} (
        契約編號,
        契約幣別,
        契約金額_外幣,
        台銀賣出匯率日期,
        台銀即期賣出匯率,
        國際貿易條件,
        約定履約日期,
        決標資訊,
        免收履約保證金,
        履約保證金繳納方式,
        履約保證金額,
        履約保證有效期限,
        免收保固保證金,
        保固保證金繳納方式,
        保固保證金額,
        保固保證有效期限,
        保固期限,
        已全部請款完畢,
        契約是否變更,
        最後契約變更日期,
        契約備註,
        契約狀態
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    # Iterate over the list and execute the query for each record
    cursor.executemany(insert_replace_sql , lst_contracts_info)
    # Commit the changes to the database
    conn.commit()
    # Close the connection
    conn.close()

    fn_log(f"driver {index} part saved to {DB_PATH} {TABLE_NAME}!")
    # driver_EPIS_contract_info.close()

# multithreading(range(int_threads), wrapper_thread_init_drivers, int_threads)
multithreading(lst_source_contracts_info, wrapper_thread, int_threads)

fn_log(f"{STR_DATESTAMP}_contracts_info_all.xlsx saved!!")
