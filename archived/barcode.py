import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
import re
import pandas as pd
import time # Import time module for adding delay
import datetime
import ast

os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''

# Define basic data
# Login variables
st_OTP_Login_URL = 'https://am.cht.com.tw/NIASLogin/faces/CHTOTP?origin_url=https%3A%2F%2Feip.cht.com.tw%2Findex.jsp'
st_MASIS_Barcode_URL = 'https://masis.cht.com.tw/IV_Net/IvQry/Inv/BarcodeQry.aspx'
# Query Barcode by Contract ID and Lot No
di_target = {"23B12A2491":["1","2"],"23C11A2301":["1"],"23F12A1381":["1","2","3","4","5","6","7","8","9","19"],"23H11A2271":["1"],"23L11A2041":["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","21","22","23","24","25","26","27","31","32","33","34","35","36","40","41","42","43","45","46","47","48","49","50","51","52","53","54","55","56","60","61","62","63","64","65","66","70","71","72","73","74","75","76","78","79","80"],"23L11A2042":["301","302","303","304","305","306","309","310","313","314","317","318","319","320","321","322","323","324","338","339","340","341","346","347","353","354","357","358","360","361"],"23M11A2001":["1","2","3","4","5","6","7","8","9","11","12","13","14","16","17","18","25","26","28","30","32","33","34","35","36","37","38","39","40","41","43","44","46","47","48","51","58","59","60","61","62","63","69","70","71","74","77","78","83","84","85","86","91","92"],"23M12A1531":["1","2","3","4","5","6","7","12","13","14","15","16","17","18","19","20","21","22","23","27","28"],"23M12A1532":["307","308","309","314","315","321","324","325"],"23N12A1111":["1"],"23U12A1101":["1","2"],"23V12A2461":["1"],"MA206A5041":["227"],"MA210A1581":["2","3","4","5","6","7","8","9","10","11","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","59","64","65","67","68","69","70","71","72","73","74","75","76","79","80","81","82","83","84","86","87","90","100","105","106","107","108","109","110","111"],"MA210A1582":["301","302","303","304","307","308","309","310","313","316","317","318","327","328","329","330","331","332","333","334"],"MA308A3961":["1","2","3","11","13","17","18","23","24","28","34","35","36","37","39","40","41","42","49","50","54","56","57","58","62","65","68","69","70","77","80","81","84","91","92","93","98","99","102","103","105","108","109","110","111","114","115","121","122","123","125","126","127","129","130","135","137","138","139","143","144","146","147","148","152","156","157","162","164","165","999"],"MA308A3963":["2","3","5","7","8","9","11"],"MA309A3091":["1","2"],"MA309A4141":["2","3","4","5","6","7","9","12","14","17","20","21","22","24","25","26","29","30","31","33","34","35","36","37","43","44","45","46","48","51","53","54","56","60","62","63","66","67","68","72","74","75","78","79","80","85","87","88","90","93","94","95","98","102","105","106","107","112","113","114","115","117","123","128","129","143","144","145","146","147","148","150"],"MA310A4311":["1","3","4","5","6","7","11","12","13","15","16","17","18","19","20","21","26","27","29","31","32","33","35","36","37","38","44","48","49","50","51","54","55","56","58","59","60","61","62","63","64","65","74","75","76","77","84","85","86","87","88","90","91","92","93","95","96","97","98","99","100","101","102","104","105","106","110","111","112","113","114","115","117","118","119","120","121","122","123","124","125","128","129","130","131","133","135","136","138","151","154","156","158","163","164","172","177","179","181","182","184","186","188","190","191","197","198","202","203","205","209","214","215","216","218","219","220","221","222","226","234","235","236","237","241","242","244","245","246","247","248","249","250","258","262","266","267","271","273","274","275","276","278","288","289","290","291","293","294","295","297","298","299","307","310","312","319"],"MA508A3951":["3","4","5","6","7","8","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","37","38","39","42","43","45","46","47","48","49","50","51","52","53","54","55","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","101","102","109","110","111","112","113","114","115","116","117","118","119","120","121","122","123","124","125","126","129","130","131","132","134","135","136","139","140","141","142","143","144","145","146","147","148","149","150","151","152","153","154","155","156","157","158","159","162","163","164","165","166","167","168","169","172"],"MA508A3952":["303","307","308","309","310","315","316","321","322","327","328","333","334","339","340"],"MA508A3954":["1","3","4","6","7","8","10","11","12","13","14","15","16"],"MA509A3641":["1"],"MA509A4061":["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","45","46","48","51","52","53","54","55","57","58","59","60","61","62","63","64","65","66","67","68","69","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","99","100","101","105","106","107","108","109","115","116","117","118","119","120","128","129","130","131","132","133","134","135","136","137","138","139","140","142","143","144","145","146","147","148","149","150","155","156","157","162","163","168","173","179","180"],"MA509A4062":["301","302","303","304","311","312","315","316","325","326","333","334","341","342","343","344","345","346","357","358","363","364","381","382","383","384","387","388"],"MA510A2431":["1"],"MA510A4261":["1","6","7","8","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","39","40","41","42","43","44","45","46","47","60","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","88","89","90","91","99","101","102","105","106","112","113","114","115","116","117","118","119","120","122","123","126","127","128","129","130","131","133","134","135","136","137","138","143","147","148","149","150","151","152","153","154","155","156","157","158","159","160","161","162","163","164","165","166","167","168","169","170","171","172","173","174","175","177","178","179","181","182","183","185","186","187","188","189","190","191","192","193","194","195","197","198","199","200","201","202","203","204","205","206","207","208","209","210","211","212","213","217","218","219","220","223","225","226","227","228","230","231","232","233","234","238","239","240","241","242","243","244","245","246","247","248","249","250","251","252","253","254","255","256","257","258","259","260","261","262","263","264","265","266","267","268","269","270","271","272","274","275","277","278","280","281","282","283","284","292","294","295","298","299","300","301","302","303","304","305","306","307","310","311","312","313","315","316","317","318","319","320","321","322","323","324","325","326","327","328","330","331","332","333","337","338","339","340","341","342","343","344","345","346","347","348","349","350","357","358","359","360","361","362","363","364","365","366","367","368","369","370","371","372","373","374","375","376","377","378","379","382","385","386","388","389","393","998"],"MA510A4262":["301","302","303","304","307","308","309","310","315","316","317","318","319","320","323","324","325","326","335","336","337","338","339","340","341","342","347","348","349","350","357","358","359","360","361","362","367","368","371","372","383","384","385","386","393","394","407","408","409","410","411","412","415","416","419","420","421","422","423","424","425","426","427","428","429","430","442","443","444","445","446","447","448","449","450","451","460","461","466","467","468","469","474","475","476","477","480","481","482","483","484","485","488","489","490","491","494","495","496","497","498","499","500","501","504","505","506","507","508","509","510","511","512","513","514","515","530","531","532","533","534","535","536","537","538","540","542","543","546","547","548","549","550","551","562","563","574","575","576","577","580","581","582","583","596","597","600","601","604","605","608","609","610","611","612","613","618","622","623","624","626","628","630","638","639","640","641","642","643","652","653","660","661","689","690","696","697","698","699"],"MA810A1571":["1","2","3","5","6","7","8","9","13","14","15","16","17","18","20","21","22","23","25","26","27","28","29","30","31","32","37","38","40","41","42","43","44"],"MAA10A2941":["1","2","3","5"],"MAR09A3071":["1","2"]}
int_total_lots = sum(len(value) for value in di_target.values())
int_finished_count = 0
# Files Path
current_time = datetime.datetime.now()
datestamp = current_time.strftime("%Y%m%d")
str_folder_path = f".\\{datestamp}\\"
os.makedirs(str_folder_path, exist_ok=True)

# Define def
def extract_table_data(int_total_pages, driver):
    li_data = []
    # initialize paging
    for page in range(1, int_total_pages + 1):
        if int_total_pages ==1:
            pass
        elif page == 1:
            try:
                # Wait for up to 1 second for the element to be present
                temp_wait_element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='1']"))
                )
            except TimeoutException:
                # If the element is not found within the timeout, jump to page 1
                driver.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder1$gv','Page$1')")
        else:
            driver.execute_script(f"__doPostBack('ctl00$ContentPlaceHolder1$gv','Page${str(page)}')")
        # get table
        table = driver.find_element(By.ID, "ContentPlaceHolder1_gv")
        html = table.get_attribute("innerHTML")
        pattern = re.compile(r'<tr class="pgr">(?:.*?<tr>.*?</tr>)*.*?</tr>', re.DOTALL)
        result = re.sub(pattern, '', html)
        result = re.sub(r'<tr>.*?</tr>', '', result, count=1, flags=re.DOTALL)
        result = re.sub(r'<tbody>|<tr>', '[', result)
        result = re.sub(r'</tbody>|</tr>', ']', result)
        result = re.sub('<[^>]+>', '"', result)
        result = result.replace(r'""', '","') 
        result = result.replace(r'][', '],[') 
        result = re.sub(r'\n|\t|&nbsp;', '', result)
        # Convert the string to a list
        result = ast.literal_eval(result)
        li_data += result
    return li_data

def fu_log(str_log, str_filename = ""):
    # Get the current date and time
    current_time = datetime.datetime.now()
    # Format the timestamp as a readable string
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    datestamp = current_time.strftime("%Y%m%d")
    # Define the log message with the timestamp
    log_message = f"{timestamp} - {str_log}\n"
    # Open the log file in append mode ('a')
    if str_filename == "":
        str_filename = f"{datestamp}_log.txt"
    with open(str_folder_path + str_filename, 'a') as log_file:
        # Write the log message to the file
        log_file.write(log_message)
    print(log_message)

# Start driver and connect to masis
edge_bin = './msedgedriver.exe'
port = 4444
service_args=[
            #   '--log-level=ALL',
            #   '--append-log',
            #   '--readable-timestamp',
              '--disable-build-check',
              ]
service = Service(executable_path=edge_bin, service_args=service_args)
options = Options()
options.add_argument('--inprivate')
driver = webdriver.Edge(service=service, options=options)
driver.get(st_OTP_Login_URL)

# Wait Login finished
temp_temp_wait_element = WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.ID, 'orientation'))
)
driver.get(st_MASIS_Barcode_URL)

for key in di_target:        
    # Input contract ID
    temp_input_element = driver.find_element(By.ID, 'ContentPlaceHolder1_txtCtId')
    temp_input_element.clear()
    temp_input_element.send_keys(key)
    for Lot in di_target.get(key):
        zfill_lot = Lot.zfill(3) if type(Lot) == str else str(Lot).zfill(3)
        int_finished_count += 1
        # Check if file already existed
        if os.path.isfile(f"{str_folder_path}{key}_{zfill_lot}.xlsx"):
            fu_log(f"{str_folder_path}{key}_{zfill_lot} already existed!!")
            continue
        try:
            fu_log(f"Fetching {key} {zfill_lot} data")
            # Input Lot No.
            temp_input_element = driver.find_element(By.ID, 'ContentPlaceHolder1_txtLotNo')
            temp_input_element.clear()
            temp_input_element.send_keys(zfill_lot)
            # Query
            temp_submit_button = driver.find_element(By.ID,'ContentPlaceHolder1_btnQry')
            temp_submit_button.click()
            time.sleep(1) # Adjust the delay as needed
            # Wait rendering
            temp_temp_wait_element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lbGvCount'))
            )
            str_page_count = temp_temp_wait_element.text
            int_pages_count = int(re.findall(r'共(.*?)頁', str_page_count)[0])
            table = driver.find_element(By.ID, "ContentPlaceHolder1_gv")
            html = table.get_attribute("innerHTML")
            # Extract table headers
            li_data = extract_table_data(int_pages_count, driver)
            # Save the DataFrame to a excel file
            df = pd.DataFrame(li_data)
            df.columns = ["材料編號", "棧板序號", "箱號", "EAN號碼", "序號", "廠商自編序號", "MAC位址", "所在庫號", "狀態", "最近領料庫號", "最近領料單號"]
            df.to_excel(f'{str_folder_path}{key}_{zfill_lot}.xlsx', index=False)
            fu_log(f"{key}_{zfill_lot}.xlsx saved!! {int_finished_count} of {int_total_lots} finished")
        except UnexpectedAlertPresentException:
            # alert = Alert(driver)
            # alert.dismiss()
            fu_log(f"{key} {zfill_lot} has no data. {int_finished_count} of {int_total_lots} finished")
            continue


test = input('Waiting: ')


driver.close()


# ------------------------------------------------
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