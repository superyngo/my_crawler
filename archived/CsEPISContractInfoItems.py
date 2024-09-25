class CsEPISContractInfoItems(CsMyDriver):
    def __init__(self):
        super().__init__()
        STR_OTP_LOGIN_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
        self.get(STR_OTP_LOGIN_URL)
        self._wait_element(By.ID, 'orientation')
        self.switch_to.window(self.window_handles[-1])
        self.close()
        self.switch_to.window(self.window_handles[0])
    def query_contract_items(self, contract:str):
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
            lst_data = self._extract_contract_items_table_data(int_total_pages)
            # to save to excel eliminate below line
            lst_data = [[contract + "_" + sublist[0], contract] + sublist for sublist in lst_data]
            return lst_data
        except TimeoutException:
            raise TimeoutException
    def _extract_contract_items_table_data(self, int_total_pages):
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
                    _result = re.sub(currency_pattern, self.replace_currency, _result)
                # Convert the string to a list
                _result = ast.literal_eval(_result)
                lst_data += _result
            return lst_data
        except TimeoutException:
            raise TimeoutException
    def query_contract_info(self, contract:str):
        BASE_URL = 'https://epis.cht.com.tw/epis100/Pages/GContract/Contract.aspx?f=G_ContractEdit&cid='
        self.get(BASE_URL + contract)
        _wait = self._wait_element(By.XPATH, f"//span[contains(text(), '契約編號：{contract}')]")
        try:
            # extract info
            return self._extract_contract_info_lists()
        except TimeoutException:
            raise TimeoutException
    def _extract_contract_info_lists(self) -> list:
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
        return  [str_契約幣別, str_契約金額_外幣, str_台銀賣出匯率日期, str_台銀即期賣出匯率, str_國際貿易條件,
                str_約定履約日期, str_決標資訊, str_免收履約保證金, str_履約保證金繳納方式, str_履約保證金額,
                str_履約保證有效期限, str_免收保固保證金, str_保固保證金繳納方式, str_保固保證金額, str_保固保證有效期限,
                str_保固期限, str_已全部請款完畢, str_契約是否變更, str_最後契約變更日期, str_契約備註, str_契約狀態]
