from modules.bin import *

# def _spit_loadable_components() -> dict[str, dict[str, Any]]:
#     def google_photo_uploader() -> dict[str, any]:
#         def google_photo_uploader_handler(self, source:dict[str, list[str]]) -> None:
#             for report in source:
#                 # fetch
#                 fn_log(f"{self._index}: Start fetching {report.prefix} {report.name} {report.postfix if report.postfix else ""}")
#                 fn_log(f"{self._index}: Fetching {report.new_name} {self._MSG_query(report = report)}!!")
#                 while not os.path.exists(report.old_path):
#                     time.sleep(3)
#                 # Rename and move
#                 try:
#                     os.rename(report.old_path, report.new_path)
#                 except:
#                     os.remove(report.old_path)
#                     fn_log(f"{report.new_path} already exists")
#                 # upload
#                 if handle_check_onlineoledll Windows only: Creates ()
#                         fn_log(f"{self._index}: Start uploading {report.new_path}, please wait for uploading.")
#                         fn_log(f"{self._index}: Upload {report.new_path} {driver_sharepoint.sharepoint_upload(report)}!!")
#     def _MSG_query(self, files:list[str]) -> None:
#                 try:
#                     # choose report
#                     for id, value in report.set_report.items():
#                         self._select_change_value(By.ID, id, value)
#                     self._select_change_value(By.ID, 'ddlReport', report.name)
#                     # wait for iframe
#                     self.switch_to.frame(self._wait_element(By.ID, "iframe"))
#                     # set report attribute
#                     for id, value in report.set_report_attribute.items():
#                         match value[0]:
#                             case 'fn_driver_select_change_value':
#                                 self._select_change_value(value[1], id, value[2])
#                                 pass
#                             case 'fn_driver_input_send_keys':
#                                 self._input_send_keys(value[1], id, value[2])
#                             case 'fn_driver_click':
#                                 self._wait_element(value[1], id).click()
#                             case _:
#                                 print('Missing procedure definition')
#                                 pass
#                     # fetch report
#                     self._wait_element(By.ID, "btnQuery").click()
#                     # check if direct download
#                     if report.show_report:
#                         str_report_handle = self.window_handles[-1]
#                         self.switch_to.window(str_report_handle)
#                         # wait report
#                         self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
#                         time.sleep(1)
#                         # download and wait
#                         try:
#                             self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
#                             self.execute_script("$find('ReportViewer1').exportReport('EXCELOPENXML');")
#                         except JavascriptException:
#                             self._wait_element(By.XPATH, f"//div[contains(text(), {report.name})]")
#                             time.sleep(5)
#                             self.execute_script("$find('ReportViewer1').exportReport('EXCELOPENXML');")
#                     # Wait for download
#                     while not os.path.exists(report.old_path):
#                         time.sleep(3)
#                     time.sleep(3)
#                     fn_log(f"{self._index}:{report.old_path} downloaded!!")
#                     # switch to main
#                     if report.show_report:
#                         self.switch_to.window(str_report_handle)
#                         self.close()
#                         self.switch_to.window(self.int_main_window_handle)
#                     # Switch back to the default content frame
#                     self.switch_to.default_content()
#                     return "succeeded"
#                 except Exception as e:
#                     return f"failed with {e}"
#         return vars()
#         def __init__component(self) -> None:
#             print('MSG component equipped!!')
#     def _loader_init_remove() -> dict[str, any]:
#         def __init__loader(self, task) -> None:
#             pass
#         def __remove__loader(self, task) -> None:
#             pass
#         return vars()
#     return {key: func() for key, func in vars().items()}

dic_uploader_config = {
    CsBasicComponent: None,
    webdriver.Edge: None,
    CsMyDriveComponent: {
      'default_args': {'./profiles/userA'}
    }
    # CsLoaderComponent: {
    #     'default_args': {'args'},
    #     'default_kwargs': {'loadable_components': _spit_loadable_components()}
    # },
    # CsMultiSeed: {
    #     'default_kwargs':{'index': 0}        
    # },
}

# dic_multi_uploader_config = {
#     CsMultiManager: {
#         'default_args': {'args', 'kwargs'},
#         'default_kwargs': {
#             'threads': 1,
#             'subclass': cs_factory(dic_uploader_config),
#         }
#     },
#     CsMultiLoaderEntry: {}
# }


