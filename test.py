# 20240920
from modules.crawlers_defs import *
from data.source_MSG_Reports import lst_source_MSG_reports


a=CsMultiCrawlersManager('MSG', config={'threads':2})
lst_test_reports = [{'name' : 'RS4183MA4L'}]
a._call_handler(handler='MSG_handler',source=lst_test_reports)

a._call('MASIS_InvQry','ALL',handler='_load_components',source=None)
a._call('ALL',handler='_remove_components',source=None)

