from modules.bin import *
import undetected_chromedriver as uc
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

import base64

class CsMyUCinit:
  def __init__(self, user_data_dir):
    user_data_dir = os.path.abspath(user_data_dir)
    os.makedirs(user_data_dir, exist_ok=True)
    # set Chrome options
    options = uc.ChromeOptions()

    # run Chrome in headless mode
    options.headless = False

    # add proxy to Chrome options
    # options.add_argument(f"--proxy-server={proxy}")
    options.unhandled_prompt_behavior = 'accept'
    # options.add_argument('--inprivate')
    # create a Chrome instance
    super(type(self),self).__init__(
        user_data_dir=user_data_dir,
        options=options,
        use_subprocess=False,
    )
    self.maximize_window()

class CsMyUCGooglePhotoUploader:
    def upload_to_google_photo(self, dict_camera:dict[str, str]):
        for camera_name, folder_path in dict_camera.items():
            hash = create_sha256_hash(self._windows_product_key + " " + self._uploader_product_key + " " + camera_name)
            api_url='https://script.google.com/macros/s/AKfycbworTnCogGbaFH20g2dn98yDwSW5lkZKiwC6INgzXNEVB3xFj5bbmXZWY20lnL1CFejTg/exec'
            encrypted_data = self._get_encrypted_data(hash, api_url)

            # 2. Decrypt the encrypted data using the hash as the key
            decrypted_json = self._decrypt_aes(encrypted_data, self._windows_product_key)

            # 3. Convert the decrypted JSON string to a dictionary
            result_dict = json.loads(decrypted_json)

            # Output the result
            print("Decrypted Data:", result_dict)


            login_email
            login_password
            album_url
            login_url = 'https://photos.google.com/login'
            self.get(login_url)
            files_path = self._list_mkv_files(folder_path)
            try:
                _wait_email_input = self._wait_element(By.XPATH, '//input[@type="text"]', 5)
            except TimeoutException:
                _wait_email_input = self._wait_element(By.XPATH, '//input[@type="email"]')
                _wait_email_input.send_keys(login_email)
                self._wait_element(By.XPATH, '//span[text()="Next" or text()="下一步" or text()="繼續"]').click()
                _wait_password_input = self._wait_element(By.XPATH, '//input[@type="password"]')
                _wait_password_input.send_keys(login_password)
                self._wait_element(By.XPATH, '//span[text()="Next" or text()="下一步" or text()="繼續"]').click()
                _wait_email_input = self._wait_element(By.XPATH, '//input[@type="text"]')
            
            self.get(album_url)
            # Locate the input element by aria-label using XPath
            _add_photo_click = self._wait_element(By.XPATH, '//button[@aria-label="新增相片"]').click()
            # Interact with the input element
            _upload_click = self._wait_element(By.XPATH, '//span[text()="從電腦中選取"]').click()
            _wait_file_input = self.find_element(By.XPATH, '//input[@type="file"]')
            _wait_file_input.send_keys(files_path)
            self._wait_element(By.XPATH, f"//div[contains(text(), '你已備份')]")
            fn_log(f"{camera_name} upload finished")
    def _list_mkv_files(self, folder_path) -> str:
        # Get all .mkv files in the folder
        mkv_files = [folder_path + file for file in os.listdir(folder_path) if file.endswith('.mkv')]
        # Join the list of files into a single string separated by newline characters
        mkv_files_str = '\n'.join(mkv_files)
        return mkv_files_str
    @property
    def _windows_product_key(self):
        import winreg
        import itertools
        # Open the registry key
        reg_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key_path) as key:
                digital_product_id = winreg.QueryValueEx(key, "BackupProductKeyDefault")[0]
                return digital_product_id
        except FileNotFoundError:
            return "Cannot find Windows product key in registry."
        except Exception as e:
            return f"Error: {e}"
    @property
    def _uploader_product_key(self):
        import winreg
        # Open the registry key
        reg_key_path = r"SOFTWARE\ANYOUNG\GOOGLEPHOTOUPLOADR"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key_path) as key:
                digital_product_id = winreg.QueryValueEx(key, "ProductKey")[0]
                return digital_product_id
        except FileNotFoundError:
            return "Cannot find uploader product key in registry."
        except Exception as e:
            return f"Error: {e}"
    # Function to get encrypted data from API
    def _get_encrypted_data(self, hash_value, api_url):
        params = {'hash': hash_value}
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}")
    # Function to decrypt AES-encrypted string
    def _decrypt_aes(self, encrypted_data, key):
        # Derive a 256-bit AES key from the hash (using SHA-256)
        key = hashlib.sha256(key.encode()).digest()

        # Decode the base64-encoded encrypted data
        encrypted_data = base64.b64decode(encrypted_data)

        # Extract the initialization vector (first 16 bytes)
        iv = encrypted_data[:16]

        # Extract the ciphertext
        ciphertext = encrypted_data[16:]

        # Create AES cipher object
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and unpad the ciphertext
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Convert bytes back to string
        return decrypted_data.decode('utf-8')
    # Convert decrypted JSON string to Python dictionary



dic_uploader_config = {
    CsBasicComponent: None,
    uc.Chrome: None,
    CsMyDriverComponent: None,
    CsMyUCinit: {
        'default_args': {'./profiles/userB'}
    },
    CsMyUCGooglePhotoUploader: None
    # CsLoaderComponent: {
    #     'default_args': {'args'},
    #     'default_kwargs': {'loadable_components': _spit_loadable_components()}
    # },
    # CsMultiSeed: {
    #     'default_kwargs':{'index': 0}        
    # },
}




