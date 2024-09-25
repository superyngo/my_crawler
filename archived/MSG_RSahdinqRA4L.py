# 20240523
from modules.crawlers_defs import *
from Python.Crawler.data.source_contracts import lst_source_contracts

FOLDER_PATH = f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\RSahdinqRA4L"
os.makedirs(FOLDER_PATH, exist_ok=True)

# Query Barcode by Contract ID and Lot No
source:list = lst_source_contracts
int_total_lots = len(source)
int_finished_count = 0

# Login to MSG 
driver_msg = Cs_MSG_Driver()

# Login to sharedrive
# driver_sharepoint = CsSharepointDriver()

# main fetch and uploading
for report in source:
    int_finished_count += 1
    report = CsMSGReport(name = 'RSahdinqRA4L', prefix = report)
    # check if exited online
    # if driver_sharepoint.check_online(report):
    #     fn_log(f"{report.new_name} already uploaded!")
    #     continue
    report.old_path = f"{STR_DOWNLOADS_FOLDER_PATH}\\{report.name}.xlsx"
    report.new_path = f"{FOLDER_PATH}\\{report.new_name}" 
    # fetch
    fn_log(f"Start fetching {report.name}.")
    fn_log(f"Fetching {report.new_name} {driver_msg.fetch_MSG_report(report)}!!")
    # Rename and move
    try:
        os.rename(report.old_path, report.new_path)
        fn_log(f"{int_finished_count} of {int_total_lots} done")
    except:
        os.remove(report.old_path)
        fn_log(f"{report.new_path} already exists")
    # upload


waiting = input('Waiting: ')

driver_msg.close()
# driver_sharepoint.close()

# region unused
    # username = input('Please enter the Username:')
    # password = input('Please enter the Password:')

    # options.binary_location = './msedgedriver.exe'
    # options.add_argument("--headless")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--user-data-dir=C:\\Users\\user\\AppData\\Local\\Microsoft\\Edge\\User Data');
    # options.add_argument('--profile-directory=Default')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    # options.add_argument('user-agent={0}'.format(user_agent))


    # Login
    # Find the username and password fields and input your credentials
    # input_username = driver.find_element(By.ID,'pt1:r1:0:it1_otplogin::content')
    # input_password = driver.find_element(By.ID,'pt1:r1:0:it2_otplogin::content')
    # input_username.send_keys(username)
    # input_password.send_keys(password)

    # print(input_username.get_attribute('value'))
    # temp_submit_button = driver.find_element(By.ID,'pt1:r1:0:cb1_otplogin')
    # temp_submit_button.click()

    # OTP_code = input('Please Enter OTP code:')
    # temp_submit_button = driver.find_element(By.ID,'d1::msgDlg::cancel')
    # temp_submit_button.click()

    # input_OTP = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, 'pt1:r1:1:s3:Focus::content'))
    # )
    # input_OTP.send_keys(OTP_code)

    # temp_submit_button = driver.find_element(By.ID,'pt1:r1:1:s3:cb2_otploginStep2')
    # temp_submit_button.click()
        # # Extract table rows
        # li_rows = table.find_elements(By.TAG_NAME, "tr")
        # # Extract data from each row
        # for row in li_rows:
        #     cols = row.find_elements(By.TAG_NAME, "td")
        #     if len(cols) == 11:
        #         li_data.append([col.text for col in cols])
        #     else:
        #         continue
        # Regular expression to match <tr class="pgr"> ... </tr> along with nested <tr> tags
    # def fn_rename_and_move(report:CsMSGReport) -> None:
    #     old_path = f"{STR_DOWNLOADS_FOLDER_PATH}\\{report.name}.xlsx"
    #     os.rename(f"{STR_DOWNLOADS_FOLDER_PATH}\\{report.name}.xlsx", f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{report.prefix}_{report.name}.xlsx")
    # 123===
# endregion