from modules.test2 import * 
# cs=webdriver.Edge
CsTest = cs_factory(dic_cs_test)
test_obj = CsTest()


from modules.test2 import * 

CsComposedLoadableDrive = cs_factory(dic_cs_cht_drive)
cht_drive = CsComposedLoadableDrive('kkk')
dir(CsComposedLoadableDrive)