"""

"""
import configparser
import os
import sys
from common import settings
import webbrowser
import subprocess


def get_config_parser():
    """
    获取配置文件读取器

    :return:
    """
    if not os.path.exists(settings.CONFIG_FILE):
        return None
    config = configparser.ConfigParser()
    config.read(settings.CONFIG_FILE)
    return config


def get_config(section: str, option: str):
    """
    读取配置文件 [config/config.ini]

    :param section:
    :param option:
    :return: 字符串类型值
    """
    config = get_config_parser()
    try:
        res = config.get(section, option)
    except:
        res = ''
    return res


def set_config(section: str, option: str, value=''):
    """
    写出配置

    :param section:
    :param option:
    :param value:
    :return:
    """
    config = get_config_parser()
    if section not in config.sections():
        config.add_section(section)
    config.set(section, option, value)
    config.write(open(settings.CONFIG_FILE, 'w+'))


def get_platform():
    """
    获取系统平台

    :return: win32 | darwin | linux
    """
    return sys.platform.lower()


def open_url_with_browser(url: str):
    """
    通过浏览器打开

    :param url: 网址
    :return:
    """
    if url is not None and url != '':
        webbrowser.open(url)


def run_cmd(cmd: str) -> tuple[int, str]:
    """
    运行命令

    :param cmd:
    :return:
    """
    code, stdout = subprocess.getstatusoutput(cmd)
    print(code, stdout)
    return code, stdout
