from modules.timestamp import *
import time, re, ast, os
import threading
from concurrent.futures import ThreadPoolExecutor
os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''
import sqlite3
LOCK = threading.Lock()

# URL and Path
STR_DOWNLOADS_FOLDER_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH = f"{STR_DOWNLOADS_FOLDER_PATH}\\{STR_DATESTAMP}"
os.makedirs(STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH, exist_ok=True)
DB_PATH = r'D:\Users\user\OneDrive - Chunghwa Telecom Co., Ltd\Work\99_共享檔案\三駐點\存控\存控.db'

def fn_log(str_log:str, str_filename:str = "") -> None:
    # Get the current date and time
    current_time = datetime.datetime.now()
    # Format the timestamp as a readable string
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # Define the log message with the timestamp
    log_message = f"{timestamp} - {str_log}\n"
    # Open the log file in append mode ('a')
    if str_filename == "":
        str_filename = f"{STR_DATESTAMP}_log.txt"
    with open(f"{STR_DOWNLOADS_TIMESTAMP_FOLDER_PATH}\\{str_filename}", 'a') as log_file:
        # Write the log message to the file
        log_file.write(log_message)
    print(log_message)

def sanitize_string(value):
    # Remove non-printable and non-ASCII characters, except for common Chinese characters and punctuation
    if isinstance(value, str):
        return re.sub(r'[^\x20-\x7E\u4E00-\u9FFF\u3000-\u303F]', '', value)
    return value

def split_list(input_list:list, num:int=1):
    # Create a list of empty lists
    result = [[] for _ in range(num)]
    # Iterate through the input list and distribute elements into sublists
    for i, val in enumerate(input_list):
        result[i % num].append(val)
    return result

def split_to_dict(source:any, num:int=1) -> dict[int, any]:
    def _list(_list, num:int=1)->dict[int, any]:
        if len(_list) < num:
            num=len(_list)
        # Create a dictionary with empty lists for each key
        result = {i: [] for i in range(num)}
        # Iterate through the input list and distribute elements into the sublists
        for i, val in enumerate(_list):
            result[i % num].append(val)
        return result
    if isinstance(source, (list,tuple)):
        return _list(source, num)
    if isinstance(source, dict):
        return {k: dict(v) for k, v in _list(source.items(), num).items()}
    raise TypeError("source must be type list, tuple or dictionary")

def create_lst_of(n:int, element={'index': None, 'driver': None, 'list': []}):
    return [element for _ in range(n)]

def multithreading(source:any, call_def:callable, threads:int=1, args:list=[], kwargs:dict={}):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        match source:
            case None:
                futures = [
                    executor.submit(call_def, *args, index=index, **kwargs)  
                    for index in list(range(threads))
                ]
            case list() | tuple() | dict():
                futures = [
                    executor.submit(call_def, *args, source=splitted_source, index=index, **kwargs)  
                    for index, splitted_source in split_to_dict(source, threads).items()
                ]
            case _:
                futures = [
                    executor.submit(call_def, *args, source=source, index=index, **kwargs) 
                    for index in list(range(threads))
                ] 
        for future in futures:
            future.result()

def convert_roc_to_western(roc_date: str = "") -> str:
    if roc_date == "":
        return ""
    # Step 1: Eliminate all non-numeric characters except "/" and "-"
    cleaned_date = re.sub(r'[^\d/-]', '', roc_date)
    # Step 2: Extract the first 3 characters (ROC year) and convert to Western year
    roc_year = int(cleaned_date[:3])
    western_year = str(roc_year + 1911)
    # Step 3: Combine Western year with the remaining part of the ROC date string
    western_date = western_year + cleaned_date[3:]
    return western_date

class DatabaseManager:
    def __init__(self, db_name):
        self._db_name = db_name
        self._conn = None
        self._cursor = None

    @property
    def sqlite(self):
        if self._cursor is None:
            raise ConnectionError("Database is not connected. Call sqlite.setter with 'connect' first.")
        return self._cursor

    @sqlite.setter
    def sqlite(self, action="connect"):
        try:
            if action == "connect":
                if self._conn is None:
                    self._conn = sqlite3.connect(self._db_name)
                    self._cursor = self._conn.cursor()
                else:
                    print("Database is already connected.")
            elif action == "close":
                if self._conn is not None:
                    self._conn.close()
                    self._conn = None
                    self._cursor = None
                else:
                    print("Database is already closed.")
            else:
                raise ValueError("Invalid action. Use 'connect' or 'close'.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self._conn = None
            self._cursor = None
            raise

    def execute_query(self, query, parameters=None):
        try:
            if self._cursor is None:
                raise ConnectionError("Database is not connected. Call sqlite.setter with 'connect' first.")
            
            if parameters:
                self._cursor.execute(query, parameters)
            else:
                self._cursor.execute(query)
            
            self._conn.commit()
            return self._cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while executing the query: {e}")
            self._conn.rollback()
            raise

    def execute_many(self, query, parameters):
        try:
            if self._cursor is None:
                raise ConnectionError("Database is not connected. Call sqlite.setter with 'connect' first.")
            
            self._cursor.executemany(query, parameters)
            self._conn.commit()
            return self._cursor.rowcount
        except sqlite3.Error as e:
            print(f"An error occurred while executing the batch query: {e}")
            self._conn.rollback()
            raise
    def write_db(self, dbname:str, columns:list[str], records:list[list]):
        insert_replace_sql = f'''
        INSERT OR REPLACE INTO {dbname} (
            {','.join(columns)}
        ) VALUES ({",".join(["?"] * len(columns))})
        '''
        try:
            if self._cursor is None:
                raise ConnectionError("Database is not connected. Call sqlite.setter with 'connect' first.")
            
            self._cursor.executemany(insert_replace_sql, records)
            self._conn.commit()
            return self._cursor.rowcount
        except sqlite3.Error as e:
            print(f"An error occurred while executing the batch query: {e}")
            self._conn.rollback()
            raise
    def __enter__(self):
        self.sqlite = "connect"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sqlite = "close"



