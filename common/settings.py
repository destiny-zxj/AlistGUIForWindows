"""

"""
import os


CONST_CONFIG_SYSTEM = 'system'
CONST_CONFIG_ALIST_BIN = 'alist_bin'
CONST_CONFIG_ALIST_PORT = 'alist_port'

CONST_IMG_APP_ICON = u':/imgs/app_icon.png'
CONST_IMG_STOP = u':/imgs/stop.png'
CONST_IMG_RUNNING = u':/imgs/running.png'
CONST_IMG_READY = u':/imgs/ready.png'
CONST_IMG_ERROR = u':/imgs/error.png'

CONST_STATUS_TXT_ERROR = '错误'
CONST_STATUS_TXT_READY = '已就绪'
CONST_STATUS_TXT_RUNNING = '正在运行'
CONST_STATUS_TXT_STOP = '已停止'

CONST_ALIST_URL = 'http://127.0.0.1'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.ini')
ALIST_DATA_DIR = os.path.join(BASE_DIR, 'data')


if not os.path.exists(ALIST_DATA_DIR):
    os.makedirs(ALIST_DATA_DIR)







