from Python.Crawler.test import * 
# cs=webdriver.Edge
CsComposedLoadableDrive = cs_factory(webdriver.Edge, **(
    spit_cs_basic_components() | spit_cs_my_drive_components() | spit_cs_loader_components(spit_cht_crawlers_loadable_components()) | spit_cs_cht_components() | spit_cs_init_components()
))
cht_crawler_drive = CsComposedLoadableDrive()


from Python.Crawler.test import * 

CsComposedLoadableDrive = cs_factory(webdriver.Edge, **(
    spit_cs_basic_components() | spit_cs_loader_components(spit_cht_crawlers_loadable_components()) | spit_cs_init_components()
))
test=CsComposedLoadableDrive()
dir(CsComposedLoadableDrive)