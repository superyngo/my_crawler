from modules.bin import *
import undetected_chromedriver as uc

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
    def upload_to_google_photo(self, login_email, login_password, album_url, folder_path):
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
    def _list_mkv_files(self, folder_path) -> str:
        # Get all .mkv files in the folder
        mkv_files = [folder_path + file for file in os.listdir(folder_path) if file.endswith('.mkv')]
        # Join the list of files into a single string separated by newline characters
        mkv_files_str = '\n'.join(mkv_files)
        return mkv_files_str

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


    # visit the test URL to check your proxy IP
