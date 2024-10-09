# 20240920
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException, NoAlertPresentException, JavascriptException
from modules.bin import *
from typing import TypedDict, Any
from types import MethodType

# source objects
class CsMyClass:
    def __init__(self, **kwargs) -> None:
        dic_default_values = {} # if default needed
        for key, value in kwargs.items():
            if key in self.__slots__:
                setattr(self, key, dic_default_values.get(key, value))
            else:
                raise AttributeError(f"'{key}' is not a valid attribute for {self.__class__.__name__}")
    def __getattr__(self, name):
        if name in self.__slots__:
            raise AttributeError(f"'{name}' was not set during initialization")
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

class CsMSGReport(CsMyClass):
    class CsSlotTypes(TypedDict):
        name: str
        prefix: str
        postfix: str
        set_report: dict[str, str]
        set_report_attribute: dict[str, str]
        handle_check_online: bool
        filename: str
        filename_extension: str
        show_report: bool
        old_path: str
        new_name: str
        new_path: str
    __slots__ = list(CsSlotTypes.__annotations__.keys())
    def __init__(self, name:str, prefix:str = None, postfix:str = None, set_report:dict = {}, set_report_attribute:dict = {}, handle_check_online:bool = True, show_report:bool = True) -> None:
        self.filename = self.name = name
        self.filename_extension = 'xlsx'
        self.postfix = postfix
        self.handle_check_online = handle_check_online
        self.show_report = show_report
        match name:
            case 'RS4183MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIV',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'ddlOrg':['fn_driver_select_change_value', By.ID, '5']
                    }
            # RS0101RA4L_NE 累積收料
            case "RS0101RA4L_NE":
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISMSH',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        "ddlOrg":['fn_driver_select_change_value', By.ID, 'M33'],
                        "txtSDate":['fn_driver_input_send_keys', By.ID, STR_START_DATE]
                    }
            # RS4212RA4L by 庫 累積領退
            case 'RS4212RA4L':
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIV',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        # 'ddlRpt':['fn_driver_select_change_value', By.ID, '0'],
                        'txtWhNo':['fn_driver_input_send_keys', By.ID, postfix]
                    }
            # RS4153RA4L 即時庫存
            case 'RS4153RA4L':
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.postfix = postfix if postfix else "all"
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIV',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'ddlWhNo1':['fn_driver_select_change_value', By.ID, '50502'],
                        'ddlWhNo2':['fn_driver_select_change_value', By.ID, '50503'],
                        'ddlWhNo3':['fn_driver_select_change_value', By.ID, '59521'],
                        'ddlWhNo4':['fn_driver_select_change_value', By.ID, '59531'],
                    }
            # RS4182M 當月庫存料月數
            case 'RS4182M':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIV',
                        }
                self.set_report_attribute = set_report_attribute 
            # RS0472MA4L 當月料庫作業量
            case 'RS0472MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISMSH',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        "ddlSOrg":['fn_driver_select_change_value', By.ID, '5']
                    }
            # RS1563MA4L 當月久未領用
            case 'RS1563MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIC',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'ddlShowDetail':['fn_driver_select_change_value', By.ID, '']
                    }
            case 'RSahdinqRA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISLP',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'txtCtId':['fn_driver_input_send_keys', By.ID, prefix]
                    }
            case 'RS5203A':
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.postfix = postfix if postfix else "all"
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISASIS',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'txtMaxPrice':['fn_driver_input_send_keys', By.ID, '9999999'],
                        'txtEDate':['fn_driver_input_send_keys', By.ID, datetime.datetime.strptime(self.prefix, '%Y%m%d').strftime('%Y/%m/%d')],
                        'ddlSOrg':['fn_driver_select_change_value', By.ID, ''],
                        'chkSelect':['fn_driver_click', By.ID],
                    }
                self.filename += STR_DATESTAMP
                self.filename_extension = 'xls'
                self.show_report = False
            case 'RS4107RA4L':
                self.prefix = prefix if prefix else STR_FIRST_DAY_OF_THIS_YEAR + "_" + STR_DATESTAMP
                self.postfix = postfix if postfix else "行通"
                self.set_report = set_report if set_report else {
                            'ddlSys':'MASIS',
                            'ddlCSys':'MASISIV',
                        }
                self.set_report_attribute = set_report_attribute if set_report_attribute else {
                        'ddlOrg':['fn_driver_select_change_value', By.ID, 'M33'],
                        'txtSDate':['fn_driver_input_send_keys', By.ID, datetime.date(DAT_TODAY.year, 1, 1).strftime("%Y/%m/%d")],
                    }
            case "_":
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.set_report = set_report
                self.set_report_attribute = set_report_attribute
        self.old_path = f"{STR_DOWNLOADS_FOLDER_PATH}\\{self.filename}.{self.filename_extension}"
        self.new_name = f"{self.prefix}_{self.filename}_{self.postfix}.{self.filename_extension}" if bool(self.postfix) else f"{self.prefix}_{self.filename}.{self.filename_extension}"
        self.new_path = f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{self.new_name}" 

def _store_crawlers_components() -> dict[str, dict[str, Any]]:
    def MSG() -> dict[str, any]:
        def MSG_handler(self, source:list[str], handle_check_online:bool=True, **kwargs) -> None:
            _BASE_URL = 'https://msgrpt.cht.com.tw/RsView12/RsPortal.aspx'
            self.get(_BASE_URL)
            # Login to sharepoint
            if handle_check_online:
                driver_sharepoint = self.__class__('sharepoint')
            # main fetch and uploading
            for report in source:
                report = CsMSGReport(**report)
                # check if exited online
                if handle_check_online and driver_sharepoint.sharepoint_check_online(report):
                    fn_log(f"{self._index}:{report.new_name} already uploaded!")
                    continue
                # fetch
                fn_log(f"{self._index}:Start fetching {report.prefix} {report.name} {report.postfix if report.postfix else ""}")
                fn_log(f"{self._index}:Fetching {report.new_name} {self._MSG_query(report = report)}!!")
                while not os.path.exists(report.old_path):
                    time.sleep(3)
                # Rename and move
                try:
                    os.rename(report.old_path, report.new_path)
                except:
                    os.remove(report.old_path)
                    fn_log(f"{report.new_path} already exists")
                # upload
                if handle_check_online:
                    fn_log(f"{self._index}:Start uploading {report.new_path}, please wait for uploading.")
                    fn_log(f"{self._index}:Upload {report.new_path} {driver_sharepoint.sharepoint_upload(report)}!!")
            if handle_check_online:
                driver_sharepoint.close()
        def _MSG_query(self, report:CsMSGReport) -> None:
                try:
                    # choose report
                    for id, value in report.set_report.items():
                        self._select_change_value(By.ID, id, value)
                    self._select_change_value(By.ID, 'ddlReport', report.name)
                    # wait for iframe
                    self.switch_to.frame(self._wait_element(By.ID, "iframe"))
                    # set report attribute
                    for id, value in report.set_report_attribute.items():
                        match value[0]:
                            case 'fn_driver_select_change_value':
                                self._select_change_value(value[1], id, value[2])
                                pass
                            case 'fn_driver_input_send_keys':
                                self._input_send_keys(value[1], id, value[2])
                            case 'fn_driver_click':
                                self._wait_element(value[1], id).click()
                            case _:
                                print('Missing procedure definition')
                                pass
                    # fetch report
                    self._wait_element(By.ID, "btnQuery").click()
                    # check if direct download
                    if report.show_report:
                        str_report_handle = self.window_handles[-1]
                        self.switch_to.window(str_report_handle)
                        # wait report
                        self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
                        time.sleep(1)
                        # download and wait
                        try:
                            self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
                            self.execute_script("$find('ReportViewer1').exportReport('EXCELOPENXML');")
                        except JavascriptException:
                            self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
                            time.sleep(5)
                            self.execute_script("$find('ReportViewer1').exportReport('EXCELOPENXML');")
                    # Wait for download
                    while not os.path.exists(report.old_path):
                        time.sleep(3)
                    time.sleep(3)
                    fn_log(f"{self._index}:{report.old_path} downloaded!!")
                    # switch to main
                    if report.show_report:
                        self.switch_to.window(str_report_handle)
                        self.close()
                        self.switch_to.window(self.int_main_window_handle)
                    # Switch back to the default content frame
                    self.switch_to.default_content()
                    return "succeeded"
                except Exception as e:
                    return f"failed with {e}"
        return vars()
        def __init__(self) -> None:
            print('MSG component equipped!!')
    def MASIS_InvQry() -> dict[str, any]:
        def MASIS_InvQry_handler(self, source:list[str], **kwargs) -> None:
            _BASE_URL = 'https://masis.cht.com.tw/IV_Net/IvQry/Inv/InvQry.aspx'
            _task_name = 'MASIS_InvQry'
            self.get(_BASE_URL)
            # main
            for txtWhno in source:     
                lst_data = []   
                fn_log(f"{self._index}:start fetching {txtWhno} inventory")
                # Input contract ID
                lst_data = self._MASIS_InvQry_query(txtWhno = txtWhno)
                with DatabaseManager(DB_PATH) as db:
                    # DELETE operation
                    db.execute_query(f"DELETE FROM {_task_name} WHERE 庫號 = '{txtWhno}'")
                    if len(lst_data) == 0:
                        fn_log(f"{self._index}:{txtWhno} has no inventory")
                        continue
                    fn_log(f"{self._index}:{txtWhno} inventory fetched")
                    # Prepare the SQL query
                    lst_sql_columns = ['項次', '庫號', '材料編號', '名稱', '料別', '呆料', '最高庫存', '實際庫存', '可用庫存', '待收數', '待退數', '待調出數', '待撥入數', '待發數', '安全存量', '上月結存數', '上月單價', '累退數', '累調出數', '累撥入數', '累領數', '料位', '管料員']
                    db.write_db(dbname=_task_name, columns=lst_sql_columns, records=lst_data)
                fn_log(f"{self._index}:{txtWhno} inventory {len(lst_data)} records saved")
        def _MASIS_InvQry_query(self, txtWhno:str) -> list:
            self._input_send_keys(By.ID, 'ContentPlaceHolder1_txtWhno', txtWhno)
            self._wait_element(By.ID, 'ContentPlaceHolder1_btnQry').click()
            time.sleep(1) # Adjust the delay as needed
            # Wait rendering
            try:
                str_pages_info = self._wait_element(By.ID, 'ContentPlaceHolder1_lbGvCount', 2).text
                int_total_pages = int(re.findall(r'共(.*?)頁', str_pages_info)[0])
                # Extract table headers
                lst_data = self._MASIS_InvQry_extract_table_html(int_total_pages = int_total_pages)
                self.refresh()
                return lst_data
            except TimeoutException:
                return []
        def _MASIS_InvQry_extract_table_html(self, int_total_pages:int) -> list:
            lst_data = []
            # initialize paging
            for page in range(1, int_total_pages + 1):
                try:
                    # Wait for up to 1 second for the element to be present
                    self._wait_element(By.XPATH, f"//span[text()='{str(page)}']", 1)
                except TimeoutException:
                    try:
                        # If the element is not found within the timeout click it
                        self._wait_element(By.XPATH, f"//a[text()='{str(page)}']", 1).click()
                        self._wait_element(By.XPATH, f"//span[text()='{str(page)}']")
                    except TimeoutException:
                        self._wait_element(By.XPATH, f"//a[text()='...']", 1).click()
                        self._wait_element(By.XPATH, f"//span[text()='{str(page)}']")
                # get table
                table = self._wait_element(By.ID, "ContentPlaceHolder1_gv0")
                html = table.get_attribute("innerHTML")
                _result = re.sub(r'<tr(.*?)</tr>', '', html, flags=re.DOTALL, count=1)
                _result = re.sub(r'<a(.*?)>|</a>|<input(.*?)>|<tr class="pgr"(.*)</tr>|\.000', '', _result, flags=re.DOTALL)
                _result = re.sub(r'<tbody>|<tr.*?>', '[', _result)
                _result = re.sub(r'</tbody>|</tr>', ']', _result)
                _result = re.sub(r'<td(.*?)>|</td>', "'", _result, flags=re.DOTALL)
                _result = _result.replace(r"''", "','")
                _result = re.sub(r'\n|\t|\s|\r', '', _result, flags=re.DOTALL)
                _result = _result.replace(r'][', '],[')
                # Convert the string to a list
                _result = self. _MASIS_InvQry_process_data(ast.literal_eval(_result))
                lst_data += _result
            return lst_data
        def _MASIS_InvQry_process_data(self, data):
            for item in data:
                # Split the third element
                third_element = item[2]
                if '(' in third_element:
                    split_elem = third_element.split('(', 1)
                    item[2] = split_elem[0]
                    item.insert(3, '(' + split_elem[1])
                # Remove the first and last letter of the fourth element (now the element at index 3)
                if len(item[3]) > 2:  # Ensure the element is long enough
                    item[3] = item[3][1:-1]
            return data
        return vars()
    def EPIS_contract_info_items() -> dict[str, any]:
        def EPIS_contract_info_items_handler(self, source:list[str], **kwargs):
            EPIS_contract_info_task_name, EPIS_contract_items_task_name = 'EPIS_contract_info', 'EPIS_contract_items'
            int_total = len(source)
            int_finished_count = 0
            DIC_COLUMNS_NAMES_CONTRACT_ITEMS = {
                12 : [['id', '契約編號', '材料編號', '名稱', '單位', '明細來源', 'IT類別', '規格', '數量', '單價', '小計', '備註'], '一般'],
                13 : [['id', '契約編號', '材料編號', '名稱', '單位', '明細來源', 'IT類別', '規格', '數量', '單價', '小計', '小計調整', '備註'], '一般'],
                15 : [['id', '契約編號', '材料編號', '名稱', '單位', '明細來源', 'IT類別', '規格', '數量', '幣別', '外幣單價', '單價', '外幣小計', '小計', '備註'], '外幣'],
                20 : [['id', '契約編號', '材料編號', '名稱', '單位', '明細來源', 'IT類別', '規格', '數量', '單價', '小計', '備註', '查型錄', '優惠計算說明', '查證方式', '查證金額', '查證結果', '契約類別', '來源契約編號', '共同供應契約資訊'], '共契']
            }
            for contract in source:
                int_finished_count += 1
                # fetch info
                lst_info_data = []
                try:
                    fn_log(f"{self._index}:Start fetching {contract} info.")
                    lst_info_data = [contract] + self._EPIS_contract_info_query(contract = contract)
                    fn_log(f"{self._index}:Fetching {contract} info succeed, proceed to fetch items.")
                except TimeoutException:
                    fn_log(f"{self._index}:{contract} has no info data. {int_finished_count} of {int_total} finished")
                    continue
                # fetch items
                lst_items_data = []
                try:
                    fn_log(f"{self._index}:Start fetching {contract} items.")
                    lst_items_data = self._EPIS_contract_items_query(contract = contract)
                    # sample out corresponding columns and type
                    lst_items_sql_columns, str_type = DIC_COLUMNS_NAMES_CONTRACT_ITEMS[len(lst_items_data[0])]
                    fn_log(f"{self._index}:{contract} items fetched. {int_finished_count} of {int_total} finished")
                except UnexpectedAlertPresentException:
                    pass
                except TimeoutException:
                    fn_log(f"{self._index}:{contract} has no items data. {int_finished_count} of {int_total} finished")
                    continue
                with DatabaseManager(DB_PATH) as db:
                    # Write contract info
                    lst_info_sql_columns = ['契約編號', '契約幣別', '契約金額_外幣', '台銀賣出匯率日期', '台銀即期賣出匯率', '國際貿易條件', '約定履約日期', '決標資訊', '免收履約保證金', '履約保證金繳納方式', '履約保證金額', '履約保證有效期限', '免收保固保證金', '保固保證金繳納方式', '保固保證金額', '保固保證有效期限', '保固期限', '已全部請款完畢', '契約是否變更', '最後契約變更日期', '契約備註', '契約狀態']
                    db.write_db(dbname=EPIS_contract_info_task_name, columns=lst_info_sql_columns, records=[lst_info_data])
                    # Write Types
                    db.execute_query(f"INSERT OR REPLACE INTO EPIS_contract_type (契約編號, 契約類別) VALUES ('{contract}', '{str_type}')")
                    # DELETE operation
                    db.execute_query(f"DELETE FROM {EPIS_contract_items_task_name} WHERE 契約編號 = '{contract}'")
                    # Write contract items
                    db.write_db(dbname=EPIS_contract_items_task_name, columns=lst_items_sql_columns, records=lst_items_data)
                fn_log(f"{self._index}:{contract} info saved to {EPIS_contract_info_task_name}!")
                fn_log(f"{self._index}:{contract} items saved to {EPIS_contract_items_task_name}!")
        # EPIS_contract_info
        def _EPIS_contract_info_query(self, contract:str) -> list:
            BASE_URL = 'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid='
            self.get(BASE_URL + contract)
            _wait = self._wait_element(By.XPATH, f"//span[contains(text(), '契約編號：{contract}')]")
            try:
                # extract info
                return self._EPIS_contract_info_extract_table_html()
            except TimeoutException:
                raise TimeoutException
        def _EPIS_contract_info_extract_table_html(self) -> list:
            str_契約幣別 = self._try_extract_element_value(By.XPATH, "//th[contains(text(), '契約幣別')]")
            str_契約金額_外幣 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl38$ctl00')
            str_台銀賣出匯率日期 = convert_roc_to_western(self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl33'))
            str_台銀即期賣出匯率 = self._try_extract_element_value(By.XPATH, "//th[contains(text(), '台銀即期賣出匯率')]")
            str_國際貿易條件 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl49')
            str_約定履約日期 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl59') + self._try_extract_element_value(By.XPATH, "//th[contains(text(), '約定履約日期')]")
            str_決標資訊 = self._try_extract_element_value(By.ID, 'ctl00_ContentPlaceHolder1_EditView_PurchaseContract_AutoLabel_AwardInfo')
            str_免收履約保證金 = self._try_extract_element_value(By.ID, 'ctl00_ContentPlaceHolder1_EditView_PurchaseContract_ctl135')
            str_履約保證金繳納方式 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl138')
            str_履約保證金額 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl140$ctl00')
            str_履約保證有效期限 = convert_roc_to_western(self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl143'))
            str_免收保固保證金 = self._try_extract_element_value(By.ID, 'ctl00_ContentPlaceHolder1_EditView_PurchaseContract_ctl146')
            str_保固保證金繳納方式 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl149')
            str_保固保證金額 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl151$ctl00')
            str_保固保證有效期限 = convert_roc_to_western(self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl154'))
            str_保固期限 = convert_roc_to_western(self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl157'))
            str_已全部請款完畢 = self._try_extract_element_value(By.ID, 'ctl00_ContentPlaceHolder1_EditView_PurchaseContract_ctl161')
            str_契約是否變更 = self._try_extract_element_value(By.ID, 'ctl00_ContentPlaceHolder1_EditView_PurchaseContract_ctl163')
            str_最後契約變更日期 = convert_roc_to_western(self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl165'))
            str_契約備註 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl167')     
            str_契約狀態 = self._try_extract_element_value(By.NAME, 'ctl00$ContentPlaceHolder1$EditView_PurchaseContract$ctl169')
            return [
                str_契約幣別, str_契約金額_外幣, str_台銀賣出匯率日期, str_台銀即期賣出匯率, str_國際貿易條件,
                str_約定履約日期, str_決標資訊, str_免收履約保證金, str_履約保證金繳納方式, str_履約保證金額,
                str_履約保證有效期限, str_免收保固保證金, str_保固保證金繳納方式, str_保固保證金額, str_保固保證有效期限,
                str_保固期限, str_已全部請款完畢, str_契約是否變更, str_最後契約變更日期, str_契約備註, str_契約狀態
            ]
        # EPIS_contract_items
        def _EPIS_contract_items_query(self, contract:str) -> list:
            try:
                BASE_URL = 'https://epis.cht.com.tw/epis100/Pages/GContract/ContractItem.aspx?f=G_ContractItem&cid='
                self.get(BASE_URL + contract)
            except UnexpectedAlertPresentException:
                time.sleep(1)
                try:
                    _input = self._wait_element(By.NAME, 'ctl00$ContentPlaceHolder1$ButtonList_Notice$ctl00', 1)
                    _input.click()
                except:
                    pass
                pass
            try:
                # Wait rendering
                str_pages_info = self._wait_element(By.CLASS_NAME, 'prev', 1).text
                int_total_pages = int(re.findall(r'/(.*?)頁', str_pages_info)[0])
                # Extract table headers
                lst_data = self._EPIS_contract_items_extract_table_html(int_total_pages = int_total_pages)
                # to save to excel eliminate below line
                lst_data = [[contract + "_" + sublist[0], contract] + sublist for sublist in lst_data]
                return lst_data
            except TimeoutException:
                raise TimeoutException
        def _EPIS_contract_items_extract_table_html(self, int_total_pages:int) -> list:
            lst_data = []
            check_currency = self._try_currency()
            # initialize paging
            try:
                for page in range(1, int_total_pages + 1):
                    # jump to page 1
                    if page == 1:
                        pass
                    else:
                        self.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder1$SortGridView_Items','Page${str(page)}')")
                    # get table
                    table = self._wait_element(By.ID, "ctl00_ContentPlaceHolder1_SortGridView_Items")
                    html = table.get_attribute("innerHTML")
                    _result = re.sub(r'<tr(.*?)</tr>', '', html, flags=re.DOTALL, count=1)
                    _result = re.sub(r'<td class="func">(.*?)disabled="disabled">(.*?)<\/td>|<span class="prefix">(.*?)</span>| title=""|">有', '', _result, flags=re.DOTALL)
                    _result = re.sub(r' class="detail" data-detail="', '>', _result)
                    _result = re.sub(r'<tbody>|<tr.*?>', '[', _result)
                    _result = re.sub(r'</tbody>|</tr>', ']', _result)
                    _result = re.sub("\'", "\\'", _result, flags=re.DOTALL)
                    _result = re.sub(r'<td class="link">.*?href="|"\starget=.*?</td>', "'", _result, flags=re.DOTALL)
                    _result = re.sub(r'<td.*?<span>|</span></td>', "'", _result, flags=re.DOTALL)
                    _result = _result.replace(r'../..', 'https://epis.cht.com.tw/epis100')
                    _result = _result.replace(r"''", "','")
                    _result = re.sub(r'\n|\t|&nbsp;|<br>|amp;|\r', '', _result)
                    _result = _result.replace(r'][', '],[')
                    if isinstance(check_currency, str) and bool(check_currency):
                        currency_pattern = f"'({check_currency})([\\d,.]+)','([\\d,.]+)','{check_currency} ([\\d,.]+)\\(([\\d,.]+)元\\)'"
                        _result = re.sub(currency_pattern, 
                            lambda match: f"'{match.group(1)}','{match.group(2)}','{match.group(3)}','{match.group(4)}','{match.group(5)}'",
                                        _result)
                    # Convert the string to a list
                    _result = ast.literal_eval(_result)
                    lst_data += _result
                return lst_data
            except TimeoutException:
                raise TimeoutException
        return vars()
    def MASIS_barcode() -> dict[str, any]:
        def MASIS_barcode_handler(self, source:dict[str,list[any]], **kwargs) -> None:
            _task_name = 'MASIS_barcode'
            STR_MASIS_BARCODE_URL = 'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx'
            self.get(STR_MASIS_BARCODE_URL)
            int_total_lots = sum(len(value) for value in source.values())
            int_finished_count = 0
            # main
            for key in source:        
                # Input contract ID
                self._input_send_keys(By.ID, 'ContentPlaceHolder1_txtCtId', key)
                for Lot in source.get(key):
                    lst_data = []
                    # zfill every lot
                    zfill_lot = Lot.zfill(3) if type(Lot) == str else str(Lot).zfill(3)
                    int_finished_count += 1
                    # Check if file already existed
                    # if os.path.isfile(f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot}.xlsx"):
                    #     fn_log(f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot} already existed!!")
                    #     continue
                    try:
                        fn_log(f"{self._index}:Fetching {key} {zfill_lot} data")
                        lst_data:list[list[str]] = [[key , zfill_lot] + lst for lst in self._MASIS_barcode_query_lot(zfill_lot)]
                        fn_log(f"{self._index}:{key} {zfill_lot} barcode fetched")
                        with DatabaseManager(DB_PATH) as db:
                            # Prepare the SQL query
                            lst_sql_columns = ['契約編號', '批次', '材料編號', '棧板序號', '箱號', 'EAN號碼', '序號', '廠商自編序號', 'MAC位址', '所在庫號', '狀態', '最近領料庫號', '最近領料單號']
                            db.write_db(dbname=_task_name, columns=lst_sql_columns, records=lst_data)
                        fn_log(f"{self._index}:{key} {zfill_lot} {len(lst_data)} barcode saved to db {_task_name}, {int_finished_count} of {int_total_lots} finished")
                    except UnexpectedAlertPresentException:
                        fn_log(f"{self._index}:{key} {zfill_lot} has no barcode. {int_finished_count} of {int_total_lots} finished")
                        continue
        def _MASIS_barcode_query_lot(self, zfill_lot:str) -> list[list[str]]:
            # Input Lot No.
            self._input_send_keys(By.ID, 'ContentPlaceHolder1_txtLotNo', zfill_lot)
            # Query
            try:
                self._wait_element(By.ID,'ContentPlaceHolder1_btnQry').click()
                time.sleep(1) # Adjust the delay as needed
                _check_alert = self.current_url
            except UnexpectedAlertPresentException:
                raise UnexpectedAlertPresentException
            # Wait rendering
            str_pages_info = self._wait_element(By.ID, 'ContentPlaceHolder1_lbGvCount').text
            int_total_pages = int(re.findall(r'共(.*?)頁', str_pages_info)[0])
            # Extract table data
            lst_data = self._MASIS_barcode_extract_table_html(int_total_pages)
            return lst_data
        def _MASIS_barcode_extract_table_html(self, int_total_pages:int) -> list[list[str]]:
            lst_data = []
            # initialize paging
            for page in range(1, int_total_pages + 1):
                if int_total_pages == 1:
                    pass
                elif page == 1:
                    try:
                        # Wait for up to 1 second for the element to be present
                        self._wait_element(By.XPATH, "//span[text()='1']", 1)
                    except TimeoutException:
                        # If the element is not found within the timeout, jump to page 1
                        self.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder1$gv','Page$1')")
                else:
                    self.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder1$gv','Page${str(page)}')")
                # get table
                table = self._wait_element(By.ID, "ContentPlaceHolder1_gv")
                html = table.get_attribute("innerHTML")
                pattern = re.compile(r'<tr class="pgr">(?:.*?<tr>.*?</tr>)*.*?</tr>', re.DOTALL)
                _result = re.sub(pattern, '', html)
                _result = re.sub(r'<tr>.*?</tr>', '', _result, count=1, flags=re.DOTALL)
                _result = re.sub(r'<tbody>|<tr>', '[', _result)
                _result = re.sub(r'</tbody>|</tr>', ']', _result)
                _result = re.sub('<[^>]+>', '"', _result)
                _result = _result.replace(r'""', '","') 
                _result = _result.replace(r'][', '],[') 
                _result = re.sub(r'\n|\t|&nbsp;', '', _result)
                # Convert the string to a list
                _result = ast.literal_eval(_result)
                lst_data += _result
            return lst_data
        return vars()
        def useless():
            # Save the DataFrame to a excel file
            # df = pd.DataFrame(lst_data)
            # df.columns = ['契約編號', '批次', '材料編號', '棧板序號', '箱號', 'EAN號碼', '序號', '廠商自編序號', 'MAC位址', '所在庫號', '狀態', '最近領料庫號', '最近領料單號']
            # df.to_excel(f'{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{key}_{zfill_lot}.xlsx', index=False)
            # fn_log(f"{key}_{zfill_lot}.xlsx saved!! {int_finished_count} of {int_total_lots} finished")
            pass
    def MASIS_item_detail() -> dict[str, any]:
        def MASIS_item_detail_handler(self, source:list[str], **kwargs):
            _task_name = 'MASIS_item_detail'
            _BASE_URL = 'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m'
            self.get(_BASE_URL)
            int_total_lots = len(source)
            int_finished_count = 0
            # main
            lst_result_items_detail = []
            for item in source:        
                int_finished_count += 1
                try:
                    fn_log(f"{self._index}:Fetching {item} details")
                    lst_item_detail = self.MASIS_item_detail_query_item(item)
                    lst_result_items_detail.append([item] +  lst_item_detail)
                    fn_log(f"{self._index}:Fetching {item} succeeded, {int_finished_count} of {int_total_lots} finished!!")
                except UnexpectedAlertPresentException:
                    fn_log(f"{self._index}:{item} doesn't exist. {int_finished_count} of {int_total_lots} queried.")
                    continue
            if len(lst_result_items_detail) == 0:
                fn_log(f"{self._index}:items has no data")
                return
            fn_log(f"{self._index}:{len(lst_result_items_detail)} items data fetched")
            with DatabaseManager(DB_PATH) as db:
                lst_sql_columns = ['材料編號', '材料名稱', '材料分類1', '材料分類2', '材料分類3', '計量單位', '追蹤週期', '導入條碼', 'EAN', '管理人員', '建檔日期', '異動日期']
                db.write_db(dbname=_task_name, columns=lst_sql_columns , records=lst_result_items_detail)
                fn_log(f"{self._index}:{len(lst_result_items_detail)} items data saved to db {_task_name}")
        def MASIS_item_detail_query_item(self, item)->list:
            # Input item NO
            self._input_send_keys(By.NAME, 'ctl00$ContentPlaceHolder1$txtMano', item)
            # Query
            self._wait_element(By.NAME,'ctl00$ContentPlaceHolder1$btnQry').click()
            # Wait rendering
            str_材料名稱 = self._wait_element(By.ID, 'ContentPlaceHolder1_txtMaName').get_attribute("value")
            str_材料分類1 = self._wait_element(By.ID, 'ContentPlaceHolder1_DDL1').get_attribute("value")
            str_材料分類2 = self._wait_element(By.ID, 'ContentPlaceHolder1_DDL2').get_attribute("value")
            str_材料分類3 = self._wait_element(By.ID, 'ContentPlaceHolder1_DDL3').get_attribute("value")
            str_計量單位 = self._wait_element(By.NAME, 'ctl00$ContentPlaceHolder1$MaUnitCtrl$ctl00').get_attribute("value")
            str_追蹤週期 = self._wait_element(By.ID, 'ContentPlaceHolder1_ddlTrace').get_attribute("value")
            str_導入條碼 = self._wait_element(By.ID, 'ContentPlaceHolder1_ddlImportReasons').get_attribute("value")
            str_EAN = self._wait_element(By.ID, 'ContentPlaceHolder1_lbEAN').text
            str_EAN.replace(";","")
            str_管理人員 = self._wait_element(By.ID, 'ContentPlaceHolder1_lbController').text
            str_建檔日期 = self._wait_element(By.ID, 'ContentPlaceHolder1_lbCrDt').text
            str_異動日期 = self._wait_element(By.ID, 'ContentPlaceHolder1_lbUpDt').text
            self.back()
            return [str_材料名稱, str_材料分類1, str_材料分類2, str_材料分類3, str_計量單位, str_追蹤週期, str_導入條碼, str_EAN, str_管理人員, str_建檔日期, str_異動日期]
        return vars()
        def useless(self):
            # Save the DataFrame to a excel file
            # df = pd.DataFrame(lst_result_items_detail)
            # df.columns = ['材料編號', '材料名稱', '材料分類1', '材料分類2', '材料分類3','計量單位', '追蹤週期', '導入條碼', 'EAN', '管理人員', '建檔日期', '異動日期']
            # df.to_excel(f'{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\item_detail/{STR_DATESTAMP}_items.xlsx', index=False)
            pass
    def EPIS_contract_batch() -> dict[str, any]:
        def EPIS_contract_batch_handler(self, source:list[str], **kwargs) -> None:
            int_total = len(source)
            int_finished_count = 0
            for contract in source:
                dict_contract_batches = None
                int_finished_count += 1
                try:
                    fn_log(f"{self._index}:Start fetching {contract} batch.")
                    dict_contract_batches = self._EPIS_contract_batch_query_contract(contract)
                except TimeoutException:
                    fn_log(f"{self._index}:{contract} has no data. {int_finished_count} of {int_total} finished")
                    continue
                if len(dict_contract_batches['data']['info']) == 0:
                    fn_log(f"{self._index}:{contract} has no data. {int_finished_count} of {int_total} finished")
                    continue
                if  dict_contract_batches['postfix'] == '外幣' and len(dict_contract_batches['data']['info'][0]) != 14:
                    dict_contract_batches['postfix'] = '類型有誤'
                # Save Contract Batch
                self._EPIS_contract_batch_save_db(dict_contract_batches)
                fn_log(f"{self._index}:{contract} batches info saved!! {int_finished_count} of {int_total} finished")
            fn_log(f"{self._index}:contract batches finished!")
            return
        def _EPIS_contract_batch_query_contract(self, contract:str):
            BASE_URL = 'https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_ContractMenu&cid='
            self.get(BASE_URL + contract)
            try:
                _wait = self._wait_element(By.ID, 'ctl00_ContentPlaceHolder1_TablePContractInfos_FormView_Content',5)
                # get batches
                _li_elements = self._wait_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                _lst_batches = [li.get_attribute('title') for li in _li_elements]
                lst_batches = [batch.split()[1] for batch in _lst_batches]
                # Extract batch details
                dic_batches_data = {
                    'contract' : contract,
                    'temp_batch' : "",
                    'data' : {
                        'info' : [],
                        '點收單' : [],
                        '收料單' : [],
                        '請款單' : []
                    },
                    'check_currency' : self._try_currency(),
                    'postfix' : '外幣' if self._try_currency() else '一般',
                }
                int_total_batches, int_fetched_batch = len(lst_batches), 0
                for batch in lst_batches:
                    dic_batches_data['temp_batch'] = batch
                    self._EPIS_contract_batch_query_batch(dic_batches_data)
                    int_fetched_batch += 1
                    fn_log(f"{self._index}:{contract}({batch}) {int_fetched_batch} / {int_total_batches} batch(es) fetched")
                return dic_batches_data
            except TimeoutException:
                raise TimeoutException
        def _EPIS_contract_batch_query_batch(self, dic_batches_data:dict) -> None:
            _table, S_mark, _物品點收單_html, _收料單_html, _請款單_html, _batch_info_html = None, None, None, None, None, None
            contract, batch = dic_batches_data['contract'], dic_batches_data['temp_batch']
            BATCH_BASE_URL = f"https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_PerformMenu&cid={contract}&pid={batch}"
            self.get(BATCH_BASE_URL)
            data = dic_batches_data['data']
            _wait = self._wait_element(By.XPATH, f"//span[contains(text(), '履約批次：{batch}')]")
            try:
                _table = self.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TablePContractBatchInfos_FormView_Content')
                S_mark = ''
            except NoSuchElementException:
                _table = self.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TablePContractBatchInfos_S_FormView_Content')
                S_mark = 'S_'
            _do = self._EPIS_contract_batch_query_batch_lists(dic_batches_data, S_mark)
            # batch info
            _batch_info_html = _table.get_attribute("innerHTML")
            lst_batch_info = self._EPIS_contract_batch_extract_batch_info(_batch_info_html, dic_batches_data['check_currency'])
            data['info'] += [[contract + "_" + batch] + [contract] + [batch] + lst_batch_info]
        def _EPIS_contract_batch_query_batch_lists(self, dic_batches_data, S_mark) -> None:
            _物品點收單_html, _收料單_html, _請款單_html = None, None, None
            contract, batch, data = dic_batches_data['contract'], dic_batches_data['temp_batch'], dic_batches_data['data']
            # 物品點收單
            _物品點收單_html = self.find_element(By.ID, f'ctl00_ContentPlaceHolder1_TableBatchInfos_{S_mark}SortGridView_ItemCheck').get_attribute('innerHTML')
            str_物品點收單 = ','.join(re.findall(r'<span>(\w{8})</span>',_物品點收單_html))
            if str_物品點收單:
                data['點收單'] += self._EPIS_contract_batch_extract_lists(_物品點收單_html, contract, batch)
            # MASIS收料單 不一定有element所以要if not S_mark
            if not S_mark:
                _收料單_html = self.find_element(By.ID, r'ctl00_ContentPlaceHolder1_TableBatchInfos_SortGridView_MasisReceive').get_attribute('innerHTML')
                str_收料單 = ','.join(re.findall(r'<span>(\w{7})</span>',_收料單_html))
            else:
                str_收料單 = ''
            if str_收料單:
                _lst = self._EPIS_contract_batch_extract_lists(_收料單_html, contract, batch)
                data['收料單'] += [[
                    convert_roc_to_western(item) if i == 5 and item else item
                    for i, item in enumerate(j)] for j in _lst
                ]
            # 請款單
            _請款單_html = self.find_element(By.ID, f'ctl00_ContentPlaceHolder1_TableBatchInfos_{S_mark}SortGridView_ApplyPay').get_attribute('innerHTML')
            str_請款單 = ','.join(re.findall(r'<span>(\w{8})</span>',_請款單_html))
            if str_請款單:
                data['請款單'] += self._EPIS_contract_batch_extract_lists(_請款單_html, contract, batch)
        def _EPIS_contract_batch_extract_batch_info(_self, html:str, check_currency) -> list:
            # basic info
            _html = re.sub(r'[\n,元]', '', html)
            if isinstance(check_currency, str) and bool(check_currency):
                pattern1 = rf'AutoLabel_BatchDatesInfo">(.*?)／(.*?)</span>.*?AutoLabel_TotalAmount">{check_currency}(.*)<br>進口匯率：(.*?)\((.*?)\).*?AutoLabel_ItemTotalAmount">{check_currency}*?(.*?)</span>'
                pattern2 = rf'.*?器材款FCA：{check_currency}(.*?)<br>.*?未稅金額\)：(.*?)<br>.*?未稅金額\)：(.*?)<br>.*?換算比例：(.*?)<br>'
                group1 = re.search(pattern1, _html).groups()
                group2 = ('', '', '', '') if re.search(pattern2, _html) is None else re.search(pattern2, _html).groups()
                _result = group1 + group2 + (re.sub(r'\\', '',check_currency),)
            else: 
                pattern = r'AutoLabel_BatchDatesInfo">(.*?)／(.*?)</span>.*?AutoLabel_TotalAmount">(.*?)</span>.*?AutoLabel_ItemTotalAmount">(.*?)</span>'
                _result = re.search(pattern, _html).groups()
            converted_result = tuple(
                convert_roc_to_western(item) if isinstance(item, str) and item.count('/') == 2 else item
                for item in _result
            )
            return list(converted_result)
        def _EPIS_contract_batch_extract_lists(_self, html:str, contract:str, batch:str) -> list[list[str]]:
            a = re.sub(r'[\n\t]|<thead>.*?</thead>|<tfoot>.*?</tfoot>|<div.*?>|</div>|元', '', html, flags=re.DOTALL)
            b = re.sub(r'<tbody>|<tr.*?>','[',a)
            c = re.sub(r'</tbody>|</tr>',']',b)
            d = re.sub(r'<td><span.*?>|</span></td>|<td.*?<a\s|"\sid.*?</td>','"',c)
            e = re.sub(r'<span.*?>|</span>', '', d)
            f = re.sub(r'href=.*?aspx&amp;','https://epis.cht.com.tw/apy/apayc.aspx?',e)
            g = re.sub(r'""','","',f)
            h = re.sub(r'\]\[','],[',g)
            i = ast.literal_eval(h)
            lst_inserted_batch = [[contract] + [batch] + sublist for sublist in i]
            return lst_inserted_batch
        _dic_EPIS_contract_batch_db_names = {
            '一般' : ['EPIS_contract_batch', ['id', '契約編號', '批次', '約定履約日期', '履約日期', '"履約金額(含稅)"', '履約明細金額總計']],
            '外幣': ['EPIS_contract_batch', ['id', '契約編號', '批次', '約定履約日期', '履約日期', '"履約金額(含稅)"', '進口匯率', '匯率日期', '履約明細金額總計', '器材款FCA', '交貨總金額', '成本分析表總價', '換算比例', '幣別']],
            '類型有誤' : None,
            '點收單' : ['EPIS_contract_batch_Pick', ['契約編號', '批次', '點收單號', '代建物品增加單', '收貨單位', '點收員工']],
            '收料單' : ['EPIS_contract_batch_RS2901RA4L', ['契約編號', '批次'',' '庫號', '庫名', '收料單號', '到料日期']],
            '請款單' : ['EPIS_contract_batch_RSapay', ['契約編號', '批次', '往請款作業', '請款單號', '類別', '狀態']]
        }
        def  _EPIS_contract_batch_save_db(self, dict_contract_batches:dict) -> None:
            data, postfix, contract = dict_contract_batches['data'], dict_contract_batches['postfix'], dict_contract_batches['contract']
            for key, value in data.items():
                if value:
                    [tablename, columns_name] = self._dic_EPIS_contract_batch_db_names[postfix] if key == 'info' else self._dic_EPIS_contract_batch_db_names[key]
                with DatabaseManager(DB_PATH) as db:
                    # Prepare the SQL query
                    lst_sql_columns = columns_name
                    insert_replace_sql = f'''
                    INSERT OR REPLACE INTO {tablename} (
                        {','.join(lst_sql_columns)}
                    ) VALUES ({",".join(["?"] * len(lst_sql_columns))})
                    '''
                    # DELETE operation
                    db.execute_query(f"DELETE FROM {tablename} WHERE 契約編號 = '{contract}'")
                    # Iterate over the list and execute the query for each record
                    db.execute_many(insert_replace_sql , value)
                    fn_log(f"{self._index}:contract batches saved to db {tablename}")
        return vars()
    def sharepoint() -> dict[str, any]:
        def sharepoint_check_online(self, source:CsMSGReport, **kwargs) ->bool:
            self.get(f"{self._sharepoint_base_url}{source.name}/")
            try:
                self._wait_element(By.XPATH, f"//button[contains(text(), '{source.new_name}')]",2)
                return True
            except:
                return False
        def sharepoint_upload(self, source:CsMSGReport, index:int = 0) -> str:
            try:
                # Clicking buttons
                self.find_element(By.CSS_SELECTOR, "button[name='上傳']").click()
                self.find_element(By.CSS_SELECTOR, "button[name='檔案']").click()
                # Waiting for 5 seconds
                time.sleep(5)
                # Sending file path to input
                file_input = self.find_element(By.CSS_SELECTOR, "input[data-automationid='commandFileInput']")
                file_input.send_keys(source.new_path)
                # Waiting for upload to complete
                self._wait_element(By.XPATH, f"//button[contains(text(), '{source.new_name}')]")
                return "succeeded"
            except Exception as e:
                return f"failed with {e}"
        _sharepoint_base_url = 'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/'
        def __init__(self) -> None:
            self.get(self._sharepoint_base_url)
            self._wait_element(By.XPATH, '//span[text()="供三採購駐點"]')
        return vars()
    def google() -> dict[str, any]:
        def __init__(self, *args, **kwargs):
            print('in google')
            print(args)
            print(kwargs)
            self.get('https://google.com')
        return vars()
    return {key: func() for key, func in vars().items()}
_crawlers_components = _store_crawlers_components()
def _store_loader_components() -> dict[str, any]:
    def _load_components(self, *args, **kwargs) -> None:
        self._loaded_components = []
        if 'ALL' in args:
            args = list(self._crawlers_components.keys())
        for task in args:
            if task in self._loaded_components:
                fn_log(f"{task} has already been loaded so skip")
                continue
            if task in list(self._crawlers_components.keys()) + ['ALL']:
                for key, value in self._crawlers_components[task].items():
                    if key == '__init__':
                        value(self)
                    else:
                        setattr(self, key, MethodType(value, self) if callable(value) else value)
            else:
                raise AttributeError(f"'{task}' is not a valid task for {self.__class__.__name__}, try {list(self._crawlers_components.keys())} or 'ALL' ")
            self._loaded_components += [task]
            fn_log(f"{task} loaded successfully")
        return None
    def _remove_components(self, *args, **kwargs) -> None:
        if 'ALL' in args:
            args = list(self._crawlers_components.keys())
        for task in args:
            if task in self._loaded_components:
                for key in self._crawlers_components[task].keys():
                    if key == '__init__':
                        continue
                    if hasattr(self, key):
                        delattr(self, key)
                self._loaded_components.remove(task)
                fn_log(f"{task} removed successfully")
            else:
                raise AttributeError(f"'{task}' components is not loaded or component {task} doesn't exists")
        return None
    return vars()
_loader_components = _store_loader_components()
def _store_common_crawlers_components() -> dict[str, any]:
    def login_cht(self) -> object:
        OTP_LOGIN_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
        self.get(OTP_LOGIN_URL)
        self._wait_element(By.ID, 'orientation')
        self.switch_to.window(self.window_handles[-1])
        self.close()
        self.switch_to.window(self.window_handles[0])
        return self
    def _try_currency(self):
        try:
            _str = self.find_element(By.XPATH, "//span[contains(text(), 'US$') or contains(text(), '€')]").text
            _pattern = r'US\$|€'
            match = re.search(_pattern, _str).group()
            if match == '€':
                return match
            return 'US\\$'
        except Exception:
            return False
    def __init__(self, *args, **kwargs) -> None:
        default = {
            'index' : 0,
            'crawlers_components' : _crawlers_components
        }
        for key, value in (default|kwargs).items():
            setattr(self, '_' + key, value)
        self._load_components(*args)
        if 'sharepoint' not in args or 'google' not in args:self.login_cht()
    return vars()
_common_crawlers_components = _store_common_crawlers_components()


# Procedures
class CsMyDriver(webdriver.Edge):
    def _select_change_value(self, By_locator:str, locator:str, new_value:str) -> None:
        _select_element = WebDriverWait(self, 20).until(EC.element_to_be_clickable((By_locator, locator)))
        _select_element = Select(_select_element)  # Create a Select instance
        _select_element.select_by_value(new_value)
    def _input_send_keys(self, By_locator:str, locator:str, new_value:str) -> None:
        _input_element = WebDriverWait(self, 20).until(EC.element_to_be_clickable((By_locator, locator)))
        _input_element.clear()
        _input_element.send_keys(new_value)
    def _wait_element(self, By_locator:str, locator:str, time:int = 1000):
        try:
            return WebDriverWait(self, time).until(EC.presence_of_element_located((By_locator, locator)))
        except UnexpectedAlertPresentException:
            try:
                self.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            return WebDriverWait(self, time).until(EC.presence_of_element_located((By_locator, locator)))
    def _try_extract_element_value(self, By_locator:str, locator:str, error_return = "") -> str:
        try:
            element = self.find_element(By_locator, locator)
            match element.tag_name:
                case 'th':
                    return element.find_element(By.XPATH, 'following-sibling::*[1]').text
                case 'input' | 'textarea':
                    if element.get_attribute('type') == 'checkbox':
                        return element.get_attribute('checked')
                    return element.get_attribute('value')
                case 'select':
                    return Select(element).first_selected_option.text
                case _:
                    return element.text
        except NoSuchElementException:
            return error_return
    def __init__(self):
        import logging
        # Suppress selenium and webdriver_manager logs
        logging.getLogger('selenium').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('webdriver_manager').setLevel(logging.WARNING)
        edge_bin = './bin/msedgedriver.exe'
        port = 4444
        service_args=[
                    #   '--log-level=ALL',
                    #   '--append-log',
                    #   '--readable-timestamp',
                    '--disable-build-check',
                    ]
        service = Service(executable_path=edge_bin, service_args=service_args)
        options = Options()
        options.add_argument('--disable-notifications')
        options.add_argument('--inprivate')
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")
        super().__init__(service=service, options=options)
        self.int_main_window_handle = self.current_window_handle

class CsDriverCrawler(CsMyDriver):
    def __init__(self, *args, basic_components=(_loader_components | _common_crawlers_components), **kwargs):
        super().__init__()
        for key, value in basic_components.items():
            if key == '__init__':
                value(self , *args, **kwargs)
            else:
                setattr(self, key, MethodType(value, self) if callable(value) else value)
        return
    def __getattr__(self, name):
        raise AttributeError(f"'{self.__class__.__name__}' '{name}' was not set")

class CsMultiCrawlersManager(CsMyClass):
    def __init__(self, *args, config={}, **kwargs): #threads=1 components=['MSG'] dic_drivers={} dic_sources={}
        print(f"args:{args}")
        print(f"config:{config}")
        print(f"kwargs:{kwargs}")
        default_config = {'threads':1, 'instances':{}, 'sources':{}, 'subclass':CsDriverCrawler, 'crawlers_components':_crawlers_components}
        for key, value in default_config.items():
            setattr(self, '_' + key, config.get(key, value))
        if args:self.args = list(args)
        if kwargs:self.kwargs = kwargs
        # init instances
        if self._threads > 0:self._init_instances(*args, crawlers_components = self._crawlers_components)
        # load components for crawlers
        self._loaded_instances_components=[]
        if args:self._load_instances_components(*args)
    def __getattr__(self, name):
        raise AttributeError(f"'{self.__class__.__name__}' '{name}' was not set")
    def _load_instances_components(self, *args, threads=None) -> None:
        if 'ALL' in args:
            args = list(self._crawlers_components.keys())
        for task in args:
            if task in self._loaded_instances_components:
                fn_log(f"{task} has already been loaded so skip")
                continue
            if task in list(self._crawlers_components.keys()) + ['ALL']:
                # load component for instances
                self._call_instances(handler='_load_components')(task)
                # set handler entrance for multi_manager
                for handler in self._crawlers_components[task].keys():
                    if not task.startswith("_"):
                        setattr(self, handler, self._call_instances(handler=handler, threads=threads))
            else:
                raise AttributeError(f"'{task}' is not a valid task for {self.__class__.__name__}, try {list(self._crawlers_components.keys())} or 'ALL' ")
            self._loaded_instances_components += [task]
            fn_log(f"{task} entry loaded successfully")
    def _remove_instances_components(self, *args) -> None:
        _args = self._loaded_instances_components.copy() if 'ALL' in args else args
        for task in _args:
            if task in self._loaded_instances_components:
                # remove component for instances
                self._call_instances('_remove_components')(task)
                for key in self._crawlers_components[task].keys():
                    if 'handler' in key and hasattr(self, key):
                        delattr(self, key)
                self._loaded_instances_components.remove(task)
                fn_log(f"{task} entry removed successfully")
            else:
                raise AttributeError(f"'{task}' components is not loaded or component {task} doesn't exists")
    def _call_instances(self, handler:str, threads:int=None):
        if self._threads==0:raise ValueError('current there is no thread')
        threads = threads if threads and threads <= self._threads else self._threads
        def _def_wrapper(*args, source:any=None, **kwargs):
            # split source into self._sources
            if isinstance(source,(list, tuple, dict)):
                self._sources = {}
                multithreading(
                    source = source,
                    call_def = lambda source, index:self._sources.update({index: source}),
                    threads = threads,
                )
            # execute instances def
            multithreading(
                source = source,
                call_def = lambda *args, index, **kwargs:getattr(self._instances[index], handler)(*args, **kwargs),
                threads = threads,
                args = args,
                kwargs = kwargs
            )
        return _def_wrapper
    @property # Getter
    def threads(self):
        return self._threads
    @threads.setter # Setter
    def threads(self, threads:int):
        if not isinstance(threads, int) or threads<0:raise TypeError(f"threads must > 0")
        match threads:
            case self._threads:
                fn_log(f"current threads {threads} unchanged")
            case _ if threads > self._threads:
                self._init_instances(*self._loaded_instances_components, threads = threads, crawlers_components = self._crawlers_components)
            case _ if threads < self._threads:
                for i in range(threads, self._threads):
                    if hasattr(self._instances[i],'close'):self._instances[i].close()
                    self._instances.pop(i)
        self._threads = threads
    def _init_instances(self, *args, threads:int=None, **kwargs):
        def _init_instance(*args, index, **kwargs):
            if index in self._instances:
                return
            self._instances.update({index:self._subclass(*args, index=index, **kwargs)})
        multithreading(
            source = None,
            call_def = _init_instance,
            threads = self._threads if threads is None else threads,
            args = args,
            kwargs = kwargs
        )
    def crawling_main(self, source, task, threads=None, **kwargs):
        fn_log(f"Total {task} count : {len(source)}")
        
        # change threads if needed
        if threads and threads > self.threads: self.threads = threads
        
        # load task
        if task not in self._loaded_instances_components : self._load_instances_components(task, threads=threads)
        
        # execute
        getattr(self, task + '_handler')(source = source, **kwargs)
def composer_factory(*args, cs=None, basic_components, main_components, super_args=[], super_kwargs={}, **kwargs):
    match cs:
        case None:
            class _():
                pass
        case _:
            class _(cs):
                pass
    def __init__(self, *args, basic_components, main_components, **kwargs):
        super().__init__(*super_args, **super_kwargs)
        for key, value in basic_components.items():
            if key == '__init__':
                value(self , *args, main_components=main_components, **kwargs)
            else:
                setattr(self, key, MethodType(value, self) if callable(value) else value)
        return
    _.__init__ = __init__
    return _(*args, **kwargs)

