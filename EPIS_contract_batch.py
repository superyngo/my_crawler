# 20240924
from modules.crawlers_defs import *
from data.source_contracts import lst_source_contracts
import pdb
lst_source_contracts = ["23S13A0041","23R13A0051"]

dic_splitted_drivers = {}
int_threads = 1
fn_log(f"Total contracts count : {len(lst_source_contracts)}")

def wrapper_contracts(index:int, source:list[str]):
    global dic_splitted_drivers
    task_name = 'EPIS_contract_batch'
    # init driver and connect to masis
    if index in dic_splitted_drivers:
        driver_crawler = dic_splitted_drivers[index].driver
        driver_crawler._load_components(task_name)
        dic_splitted_drivers[index].data = source
    else:
        dic_splitted_drivers[index] = CsSplittedDrivers(driver = CsDriverCrawler(task_name).login_cht(), data = source)
        driver_crawler = dic_splitted_drivers[index].driver
    driver_crawler.EPIS_contract_batch_handler(source = source, index = index)

def main():
    multithreading(lst_source_contracts, wrapper_contracts, int_threads)
    fn_log(f'{len(lst_source_contracts)} contracts batch saved!!')

if __name__ == "__main__":
    main()

pdb.set_trace()

# # CONTRACT_BATCH_TABLE_NAME = r'T_Contract_Batch'
# # CONTRACT_BATCH_PICK_TABLE_NAME = r'T_Contract_Batch_Pick'
# # CONTRACT_BATCH_RS2901RA4L_TABLE_NAME = r'T_Contract_Batch_RS2901RA4L'
# # CONTRACT_BATCH_RSapay_TABLE_NAME = r'T_Contract_Batch_RSapay'

# # test
# lst_source_contracts_batches = lst_source_contracts
# # ['23N13A0311', '23V13A0301', '23R13A0322', '23C13A0352', '23Q13A0382', '23A13A0402', '23X13A0423', '23D13A0491', '23M13A0521', '23T13A0531', '23G13A0581', '23G13A0641', '23U13A0652', '23V13A0741', '23E13A0691', '23J13A0871', '23A13A0822', '23X13A0592', '23Q13A0971', '23X13A0992', '23D13A1022', '23Z13A1051', '23C13A1071', '23K13A1151', '23J13A1171', '23F13A1281', '23B13A1301', '23J13A1292', '23J13A1295', '23D13A1211', '23C13A1312', '23A13A1331', '23V13A1372', '23T13A1223', '23K13A1381', '23Y13A1422', '23N13A1461', '23S13A1491', '23U13A1521', '23R13A1501', '23Q13A1441', '23D13A1562', '23V13A1601', '23U13A1651', '23N13A1661', '23Q13A1691', '23E13A1701', '23Y13A1781', '23F13A1391', '23B13A1792', '23W13A1811', '23G13A18313U13A1651', '23N13A1661', '23Q13A1691', '23E13A1701', '23Y13A1781', '23F13A1391', '23B13A1792', '23W13A1811', '23G13A1831', '23E13A1891', '23T13A1932', '23U13A1941', '23D13A1981', '23N13A2001', '23Y13A2061', '23Q13A2081', '23B13A2111', '23U13A2131', '23D13A2201', '23Y13A2221', '23I13A2261', '23G13A2292', '23E13A2321', '23T13A2341', '23Q13A0811', '23B13A2382', '23Q13A2391', '23I13A2451', '23I13A2521', '23W13A2281']
# # driver_EPIS_contract_batch = CsEPISContractBatch()
# # dict_contract_batches = driver_EPIS_contract_batch.query_contract_batch("23E11A0331")

# int_total = len(lst_source_contracts_batches)
# int_finished_count = 0
# dic_drivers = {}
# int_threads = 2

# def wrapper_thread(index, source):
#     global int_total, int_finished_count, dic_drivers
#     # Start driver and connect to masis
#     if index in dic_drivers:
#         driver_EPIS_contract_batch = dic_drivers[index] 
#     else:
#         driver_EPIS_contract_batch = dic_drivers[index] = CsEPISContractBatch()
#     # main
#     # Connect to the SQLite database
#     conn = sqlite3.connect(DB_PATH)
#     for contract in source:
#         dict_contract_batches = None
#         with LOCK:
#             int_finished_count += 1
#         try:
#             fn_log(f"driver {index}:Start fetching {contract} batch.")
#             dict_contract_batches = driver_EPIS_contract_batch.query_contract_batch(contract)
#         except TimeoutException:
#             fn_log(f"driver {index}:{contract} has no data. {int_finished_count} of {int_total} finished")
#             continue
#         if len(dict_contract_batches['data']['info']) == 0:
#             fn_log(f"driver {index}:{contract} has no data. {int_finished_count} of {int_total} finished")
#             continue
#         if  dict_contract_batches['postfix'] == '外幣' and len(dict_contract_batches['data']['info'][0]) != 14:
#             dict_contract_batches['postfix'] = '類型有誤'
#         # Save Contract Batch
#         driver_EPIS_contract_batch.save_db(dict_contract_batches, conn)
#         fn_log(f"driver {index}:{contract} batches info saved!! {int_finished_count} of {int_total} finished")
#     # Close the connection
#     conn.close()
#     fn_log(f"driver {index} part finished!")
#     test = input('Waiting: ')

# multithreading(lst_source_contracts_batches, wrapper_thread, int_threads)



