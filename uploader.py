from modules.uploader import *

upload_config = {
  'no1' : 'C:/Users/user/Downloads/',
}

CsUCdriver = cs_factory(dic_uploader_config)
UCdriver = CsUCdriver()
UCdriver.upload_to_google_photo(upload_config)
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