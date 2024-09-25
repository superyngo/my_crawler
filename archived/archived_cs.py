from modules.timestamp import *
from selenium.webdriver.common.by import By
class Cs_Report:
    def __init__(self, name:str, prefix:str = None, postfix:str = None, process:dict = {}) -> None:
        self.name = name
        self.postfix = postfix
        match name:
            case 'RS4183MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISIV',
                        },
                    'set_report_attribute' : {
                        'ddlOrg':['fn_driver_select_change_value', By.ID, '5']
                    }
                }
            # RS0101RA4L_NE 累積收料
            case "RS0101RA4L_NE":
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.process = {
                    "set_report" : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISMSH',
                        },
                    "set_report_attribute" : {
                        "ddlOrg":['fn_driver_select_change_value', By.ID, 'M33'],
                        "txtSDate":['fn_driver_input_send_keys', By.ID, STR_START_DATE]
                    }
                }
            # RS4212RA4L by 庫 累積領退
            case 'RS4212RA4L':
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISIV',
                        },
                    'set_report_attribute' : {
                        "ddlRpt":['fn_driver_select_change_value', By.ID, '1'],
                        'txtWhNo':['fn_driver_input_send_keys', By.ID, postfix]
                    }
                }
            # RS4153RA4L 即時庫存
            case 'RS4153RA4L':
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISIV',
                        },
                    'set_report_attribute' : {
                        'ddlWhNo1':['fn_driver_select_change_value', By.ID, '50502'],
                        'ddlWhNo2':['fn_driver_select_change_value', By.ID, '50503'],
                        'ddlWhNo3':['fn_driver_select_change_value', By.ID, '59521'],
                        'ddlWhNo4':['fn_driver_select_change_value', By.ID, '59531'],
                    }
                }
            # RS4182M 當月庫存料月數
            case 'RS4182M':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISIV',
                        },
                    'set_report_attribute' : {}
                }
            # RS0472MA4L 當月料庫作業量
            case 'RS0472MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISMSH',
                        },
                    'set_report_attribute' : {
                        "ddlSOrg":['fn_driver_select_change_value', By.ID, '5']
                    }
                }
            # RS1563MA4L 當月久未領用
            case 'RS1563MA4L':
                self.prefix = prefix if prefix else STR_THIS_MONTH_PREFIX
                self.process = {
                    'set_report' : {
                        'ddlSys':'MASIS',
                        'ddlCSys':'MASISIC',
                        },
                    'set_report_attribute' : {
                        'ddlShowDetail':['fn_driver_select_change_value', By.ID, '']
                    }
                }
            case "_":
                self.prefix = prefix if prefix else STR_DATESTAMP
                self.process = {
                    'set_report' : {},
                    'set_report_attribute' : {}
                }
        self.process = process if process else self.process
        self.process['set_report']['ddlReport'] = name
        self.new_name = f"{self.prefix}_{name}_{postfix}.xlsx" if bool(postfix) else f"{self.prefix}_{name}.xlsx"

class CsSharepointDriver(CsMyDriver):
    def check_online(self, report:CsMSGReport) -> bool:
        self.get(f"{self._STR_SHAREPOINT_URL}{report.name}/")
        try:
            self._wait_element(By.XPATH, f"//button[contains(text(), '{report.new_name}')]",2)
            return True
        except:
            return False
    def upload(self, report:CsMSGReport) -> None:
        try:
            # Clicking buttons
            self.find_element(By.CSS_SELECTOR, "button[name='上傳']").click()
            self.find_element(By.CSS_SELECTOR, "button[name='檔案']").click()
            # Waiting for 5 seconds
            time.sleep(5)
            # Sending file path to input
            file_input = self.find_element(By.CSS_SELECTOR, "input[data-automationid='commandFileInput']")
            file_input.send_keys(report.new_path)
            # Waiting for upload to complete
            self._wait_element(By.XPATH, f"//button[contains(text(), '{report.new_name}')]")
            return "succeeded"
        except Exception as e:
            return f"failed with {e}"
    def __init__(self):
        super().__init__()
        self._STR_SHAREPOINT_URL = 'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/'
        self.get(self._STR_SHAREPOINT_URL)
        self._wait_element(By.XPATH, '//span[text()="供三採購駐點"]')


class CsMASISBarcode(CsMyDriver):
    def extract_table_html(self, int_total_pages:int):
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
    def query_lot(self, zfill_lot:str):
        # Input Lot No.
        self._input_send_keys(By.ID, 'ContentPlaceHolder1_txtLotNo', zfill_lot)
        # Query
        self._wait_element(By.ID,'ContentPlaceHolder1_btnQry').click()
        time.sleep(1) # Adjust the delay as needed
        # Wait rendering
        str_pages_info = self._wait_element(By.ID, 'ContentPlaceHolder1_lbGvCount').text
        int_total_pages = int(re.findall(r'共(.*?)頁', str_pages_info)[0])
        # Extract table headers
        lst_data = self.extract_table_html(int_total_pages)
        return lst_data
    def __init__(self):
        super().__init__()
        STR_OTP_LOGIN_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
        STR_MASIS_BARCODE_URL = 'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx'
        self.get(STR_OTP_LOGIN_URL)
        self._wait_element(By.ID, 'orientation')
        self.switch_to.window(self.window_handles[-1])
        self.close()
        self.switch_to.window(self.window_handles[0])
        self.get(STR_MASIS_BARCODE_URL)
        self.Whno = ["50502","50503","59511","59512","59521","59531"]
class CsMASISItemDetail(CsMyDriver):
    def query_item(self, item)->list:
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
    def __init__(self):
        super().__init__()
        STR_OTP_LOGIN_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
        STR_MASIS_ITEM_DETAIL_URL = 'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m'
        self.get(STR_OTP_LOGIN_URL)
        self._wait_element(By.ID, 'orientation')
        self.switch_to.window(self.window_handles[-1])
        self.close()
        self.switch_to.window(self.window_handles[0])
        self.get(STR_MASIS_ITEM_DETAIL_URL)
class CsEPISContractBatch(CsMyDriver):
    def __init__(self):
        super().__init__()
        STR_OTP_LOGIN_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
        self.get(STR_OTP_LOGIN_URL)
        self._wait_element(By.ID, 'orientation')
        self.switch_to.window(self.window_handles[-1])
        self.close()
        self.switch_to.window(self.window_handles[0])
    def query_contract_batch(self, contract:str):
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
                self._query_batch(dic_batches_data)
                int_fetched_batch += 1
                fn_log(f"{contract}({batch}) {int_fetched_batch} / {int_total_batches} batch(es) fetched")
            return dic_batches_data
        except TimeoutException:
            raise TimeoutException
    def _query_batch(self, dic_batches_data:dict) -> None:
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
        _do = self._query_batch_lists(dic_batches_data, S_mark)
        # batch info
        _batch_info_html = _table.get_attribute("innerHTML")
        lst_batch_info = self._extract_batch_info(_batch_info_html, dic_batches_data['check_currency'])
        data['info'] += [[contract + "_" + batch] + [contract] + [batch] + lst_batch_info]
    def _extract_batch_info(self, html:str, check_currency) -> list:
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
    def _query_batch_lists(self, dic_batches_data, S_mark) -> None:
        _物品點收單_html, _收料單_html, _請款單_html = None, None, None
        contract, batch, data = dic_batches_data['contract'], dic_batches_data['temp_batch'], dic_batches_data['data']
        # 物品點收單
        _物品點收單_html = self.find_element(By.ID, f'ctl00_ContentPlaceHolder1_TableBatchInfos_{S_mark}SortGridView_ItemCheck').get_attribute('innerHTML')
        str_物品點收單 = ','.join(re.findall(r'<span>(\w{8})</span>',_物品點收單_html))
        if str_物品點收單:
            data['點收單'] += self._extract_lists(_物品點收單_html, contract, batch)
        # MASIS收料單 不一定有element所以要if not S_mark
        if not S_mark:
            _收料單_html = self.find_element(By.ID, r'ctl00_ContentPlaceHolder1_TableBatchInfos_SortGridView_MASISReceive').get_attribute('innerHTML')
            str_收料單 = ','.join(re.findall(r'<span>(\w{7})</span>',_收料單_html))
        else:
            str_收料單 = ''
        if str_收料單:
            _lst = self._extract_lists(_收料單_html, contract, batch)
            data['收料單'] += [[
                convert_roc_to_western(item) if i == 5 and item else item
                for i, item in enumerate(j)] for j in _lst
            ]
        # 請款單
        _請款單_html = self.find_element(By.ID, f'ctl00_ContentPlaceHolder1_TableBatchInfos_{S_mark}SortGridView_ApplyPay').get_attribute('innerHTML')
        str_請款單 = ','.join(re.findall(r'<span>(\w{8})</span>',_請款單_html))
        if str_請款單:
            data['請款單'] += self._extract_lists(_請款單_html, contract, batch)
    def _extract_lists(self, html:str, contract:str, batch:str) -> list:
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
    dic_db_names = {
        '一般' : ['T_Contract_Batch', 'id, 契約編號, 批次, 約定履約日期, 履約日期, "履約金額(含稅)", 履約明細金額總計'],
        '外幣': ['T_Contract_Batch', 'id, 契約編號, 批次, 約定履約日期, 履約日期, "履約金額(含稅)", 進口匯率, 匯率日期, 履約明細金額總計, 器材款FCA, 交貨總金額, 成本分析表總價, 換算比例, 幣別'],
        '類型有誤' : None,
        '點收單' : ['T_Contract_Batch_Pick', '契約編號, 批次, 點收單號, 代建物品增加單, 收貨單位, 點收員工'],
        '收料單' : ['T_Contract_Batch_RS2901RA4L', '契約編號, 批次, 庫號, 庫名, 收料單號, 到料日期'],
        '請款單' : ['T_Contract_Batch_RSapay', '契約編號, 批次, 往請款作業, 請款單號, 類別, 狀態']
    }
    def save_db(self, dict_contract_batches:dict, conn) -> None:
        cursor = conn.cursor()
        data, postfix, contract = dict_contract_batches['data'], dict_contract_batches['postfix'], dict_contract_batches['contract']
        for key, value in data.items():
            if value:
                [tablename, columnsnames] = self.dic_db_names[postfix] if key == 'info' else self.dic_db_names[key]
                int_len_of_lst = len(value[0])
                # Prepare the SQL query
                insert_replace_sql  = f'''
                INSERT OR REPLACE INTO {tablename} (
                    {columnsnames}
                ) VALUES ({",".join(["?"] * int_len_of_lst)})
                '''
                # DELETE operation
                cursor.execute(f"DELETE FROM {tablename} WHERE 契約編號 = '{contract}'")
                # Iterate over the list and execute the query for each record
                cursor.executemany(insert_replace_sql , value)
                # Commit the changes to the database
                conn.commit()

def useless():
    dic_URLs = {
        'MSG':'https://msgrpt.cht.com.tw/RsView12/RsPortal.aspx',
        'MASIS_InvQry':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/InvQry.aspx',
        'EPIS_contract_info_URL':'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid=',
        'EPIS_contract_items_URL':'https://epis.cht.com.tw/epis100/Pages/GContract/ContractItem.aspx?f=G_ContractItem&cid=',
        'SHAREPOINT':'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/',
        'MASIS_BARCODE':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx',
        'MASIS_ITEM_DETAIL':'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m',
        'EPIS_contract_batch':'https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_ContractMenu&cid=',
    }

        dic_storage = {
            'MSG':CsCrawlerResources(**{
                'URL':'https://msgrpt.cht.com.tw/RsView12/RsPortal.aspx',
                'handler':MSG_handler,
                '_query':MSG_query,
            }),
            'MASIS_InvQry':CsCrawlerResources(**{
                'URL':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/InvQry.aspx',
                'handler':MASIS_InvQry_handler,
                '_query':MASIS_InvQry_query,
                '_extract_table_html':MASIS_InvQry_extract_table_html
            }),
            'EPIS_contract_info_items':CsCrawlerResources(**{
                'handler':EPIS_contract_info_items_handler,
            }),
            'EPIS_contract_info':CsCrawlerResources(**{
                'URL':'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid=',
                '_query':EPIS_contract_info_query,
                '_extract_table_html':EPIS_contract_info_extract_table_html,
            }),
            'EPIS_contract_items':CsCrawlerResources(**{
                'URL':'https://epis.cht.com.tw/epis100/Pages/GContract/ContractItem.aspx?f=G_ContractItem&cid=',
                '_query':EPIS_contract_items_query,
                '_extract_table_html':EPIS_contract_items_extract_table_html
            })
        }
        dic_URLs = {
                'SHAREPOINT':'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/',
                'MASIS_BARCODE':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx',
                'MASIS_ITEM_DETAIL':'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m',
                'EPIS_contract_batch':'https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_ContractMenu&cid=',
            }
    pass