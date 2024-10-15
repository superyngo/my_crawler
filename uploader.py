from modules.uploader import *

upload_config = {
  'folder_path' : 'C:/Users/user/Downloads/',
  'album_url' : 'https://photos.google.com/u/0/share/AF1QipN5ErAyjjFPCxWgw--uYgbrvJWZu1U39-3iyeChyQQv0PDxU59NnyNP_k4bZNMrvw',
  'login_email' : 'superyngo2@gmail.com',
  'login_password' : '951753qSceSz2'
}

CsUCdriver = cs_factory(dic_uploader_config)
UCdriver = CsUCdriver()
UCdriver.upload_to_google_photo(**upload_config)
UCdriver.quit()

# 1.init args
# 1.1 bowser profile or cookies
# 2.album url
# 3.list of files
# 4.login informations
# 5.


# api
# pc name and windows key => hash
# return login informations