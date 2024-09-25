# 20240923
from modules.crawlers_defs import *

# Query Barcode by Contract ID and Lot No
source = {"23B12A2491":["1","2",3,4,5]}

driver_crawler = CsDriverCrawler('MASIS_barcode').login_cht()
driver_crawler.MASIS_barcode_handler(source=source)


# int_total_lots = sum(len(value) for value in di_target.values())
# int_finished_count = 0

# # Start driver and connect to masis
# driver_barcode = CsMASISBarcode()

# # main
# for key in di_target:        
#     # Input contract ID
#     driver_barcode._input_send_keys(By.ID, 'ContentPlaceHolder1_txtCtId', key)
#     for Lot in di_target.get(key):
#         # zfill every lot
#         zfill_lot = Lot.zfill(3) if type(Lot) == str else str(Lot).zfill(3)
#         int_finished_count += 1
#         # Check if file already existed
#         if os.path.isfile(f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot}.xlsx"):
#             fn_log(f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot} already existed!!")
#             continue
#         try:
#             fn_log(f"Fetching {key} {zfill_lot} data")
#             li_data = driver_barcode.query_lot(zfill_lot)
#             # Save the DataFrame to a excel file
#             df = pd.DataFrame(li_data)
#             df.columns = ["材料編號", "棧板序號", "箱號", "EAN號碼", "序號", "廠商自編序號", "MAC位址", "所在庫號", "狀態", "最近領料庫號", "最近領料單號"]
#             df.to_excel(f'{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot}.xlsx', index=False)
#             fn_log(f"{key}_{zfill_lot}.xlsx saved!! {int_finished_count} of {int_total_lots} finished")
#         except UnexpectedAlertPresentException:
#             fn_log(f"{key} {zfill_lot} has no data. {int_finished_count} of {int_total_lots} finished")
#             continue

# test = input('Waiting: ')
# driver_barcode.close()
