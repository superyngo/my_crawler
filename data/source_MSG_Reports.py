from modules.crawlers_defs import *


lst_source_MSG_reports:list = [
    # RS4183MA4L 當月收領料、庫存
    {'name' : 'RS4183MA4L'},
    # RS0101RA4L_NE 累積收料
    {'name' : 'RS0101RA4L_NE'},
    # RS4212RA4L 50503 累積領退
    {
    'name' : 'RS4212RA4L', 
    'postfix' : '50503'
    },
    # RS4212RA4L 59511 累積領退
    {
    'name' : 'RS4212RA4L', 
    'postfix' : '59511'
    },
    # RS4212RA4L 59512 累積領退
    {
    'name' : 'RS4212RA4L', 
    'postfix' : '59512'
    },
    # RS4212RA4L 59521 累積領退
    {
    'name' : 'RS4212RA4L', 
    'postfix' : '59521'
    },
    # RS4212RA4L 59531 累積領退
    {
    'name' : 'RS4212RA4L', 
    'postfix' : '59531'
    },
    # RS4153RA4L 行北
    {
        'name' : 'RS4153RA4L',
        'set_report_attribute' : {
                        'ddlWhNo1':['fn_driver_select_change_value', By.ID, '50503'],
                        'ddlWhNo2':['fn_driver_select_change_value', By.ID, '59511'],
                        'ddlWhNo3':['fn_driver_select_change_value', By.ID, '59512'],
                        'ddlWhNo4':['fn_driver_select_change_value', By.ID, ''],
                    },
        'postfix' : '行北'
    },
    # RS4153RA4L 行中南
    {
        'name' : 'RS4153RA4L',
        'set_report_attribute' : {
                        'ddlWhNo1':['fn_driver_select_change_value', By.ID, '59521'],
                        'ddlWhNo2':['fn_driver_select_change_value', By.ID, '59531'],
                        'ddlWhNo3':['fn_driver_select_change_value', By.ID, ''],
                        'ddlWhNo4':['fn_driver_select_change_value', By.ID, ''],
                    },
        'postfix' : '行中南'
    },
    # RS4182M 當月庫存料月數
    {'name' : 'RS4182M'},
    # RS0472MA4L 當月料庫作業量
    {'name' : 'RS0472MA4L'},
    # RS1563MA4L 當月久未領用
    {'name' : 'RS1563MA4L'},
    # RS5203A 全區契約今年至今
    {'name' : 'RS5203A'},
    # 行通料庫進出
    {'name' : 'RS4107RA4L'}
]
