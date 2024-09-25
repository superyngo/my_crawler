# 20240920
from modules.crawlers_defs import *

a  =CsMultiCrawlersManager(config={'threads':1,'subclass':test}, k=1)
a._call_instances(handler='bark')('bark')
a._call_instances(handler='woof')()
a.change_threads(3)


a=CsMultiCrawlersManager('MSG', config={'threads':2})
lst_test_reports = [{'name' : 'RS4183MA4L'}]
a._call_instances(handler='MSG_handler',source=lst_test_reports)

a._call_instances('MASIS_InvQry','ALL',handler='_load_components',source=None)
a._call_instances('ALL',handler='_remove_components',source=None)
a._call_instances(handler='bark', source=None, args=[1,2,3], kwargs = {1:1,2:2})

