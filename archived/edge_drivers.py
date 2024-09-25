# 20240902
from modules.crawlers_defs import *
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
    def _try_extract_element_value(self, By_locator:str, locator:str, error_return = ""):
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

# Procedures
class CsDriverCrawler(CsMyDriver):
    def __init__(self, *args):
        super().__init__()
        self._loaded_components = []
        self._load_components(*args)
        return None
    def __getattr__(self, name):
        raise AttributeError(f"'{self.__class__.__name__}' '{name}' was not set")
    def _load_components(self, *args) -> None:
        if 'ALL' in args:
            args = list(dic_components.keys())
        for task in args:
            if task in self._loaded_components:
                fn_log(f"{task} has already been loaded so skip")
                continue
            if task in list(dic_components.keys()) + ['ALL']:
                for key, value in dic_components[task].items():
                    if key == '__init__':
                        value(self)
                    else:
                        setattr(self, key, MethodType(value, self) if callable(value) else value)
            else:
                raise AttributeError(f"'{task}' is not a valid task for {self.__class__.__name__}, try {list(dic_components.keys())} or 'ALL' ")
            self._loaded_components += [task]
            fn_log(f"{task} loaded successfully")
        return None
    def _remove_components(self, *args) -> None:
        if 'ALL' in args:
            args = list(dic_components.keys())
        for task in args:
            if task in self._loaded_components:
                for key in dic_components[task].keys():
                    if key == '__init__':
                        continue
                    if hasattr(self, key):
                        delattr(self, key)
                self._loaded_components.remove(task)
                fn_log(f"{task} removed successfully")
            else:
                raise AttributeError(f"'{task}' components is not loaded or component {task} doesn't exists")
        return None
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
    def _process_data(self, data):
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

# dic_URLs = {
#     'MSG':'https://msgrpt.cht.com.tw/RsView12/RsPortal.aspx',
#     'MASIS_InvQry':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/InvQry.aspx',
#     'EPIS_contract_info_URL':'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid=',
#     'EPIS_contract_items_URL':'https://epis.cht.com.tw/epis100/Pages/GContract/ContractItem.aspx?f=G_ContractItem&cid=',
#     'SHAREPOINT':'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/',
#     'MASIS_BARCODE':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx',
#     'MASIS_ITEM_DETAIL':'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m',
#     'EPIS_contract_batch':'https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_ContractMenu&cid=',
# }

#     dic_storage = {
#         'MSG':CsCrawlerResources(**{
#             'URL':'https://msgrpt.cht.com.tw/RsView12/RsPortal.aspx',
#             'handler':MSG_handler,
#             '_query':MSG_query,
#         }),
#         'MASIS_InvQry':CsCrawlerResources(**{
#             'URL':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/InvQry.aspx',
#             'handler':MASIS_InvQry_handler,
#             '_query':MASIS_InvQry_query,
#             '_extract_table_html':MASIS_InvQry_extract_table_html
#         }),
#         'EPIS_contract_info_items':CsCrawlerResources(**{
#             'handler':EPIS_contract_info_items_handler,
#         }),
#         'EPIS_contract_info':CsCrawlerResources(**{
#             'URL':'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid=',
#             '_query':EPIS_contract_info_query,
#             '_extract_table_html':EPIS_contract_info_extract_table_html,
#         }),
#         'EPIS_contract_items':CsCrawlerResources(**{
#             'URL':'https://epis.cht.com.tw/epis100/Pages/GContract/ContractItem.aspx?f=G_ContractItem&cid=',
#             '_query':EPIS_contract_items_query,
#             '_extract_table_html':EPIS_contract_items_extract_table_html
#         })
#     }
#     dic_URLs = {
#             'SHAREPOINT':'https://cht365.sharepoint.com/sites/msteams_e919c5/Shared Documents/General/存控/0_DB/',
#             'MASIS_BARCODE':'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx',
#             'MASIS_ITEM_DETAIL':'https://masis.cht.com.tw/masis/NM/Mano/ManoMtn.aspx?t=m',
#             'EPIS_contract_batch':'https://epis.cht.com.tw/epis100/Pages/GContract/_Menu.aspx?f=G_ContractMenu&cid=',
#         }
