# -*- coding: UTF-8 -*-
"""
@Project :volatility3_gui_fz 
@File    :config
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/9/2 下午4:46 
"""
import configparser
import os.path


def _check_config_ini():
    if not os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def read_config_ini():
    _check_config_ini()
    config = configparser.ConfigParser()
    # 尝试读取现有的配置文件
    if os.path.exists("config.ini"):
        config.read('config.ini')
    return config['DEFAULT']


def write_config_ini(key, value):
    _check_config_ini()
    config = configparser.ConfigParser()
    # 尝试读取现有的配置文件
    config.read('config.ini')
    config['DEFAULT'][key] = value

    # 将更新后的配置写回文件
    with open('config.ini', 'w') as configfile:
        config.write(configfile)



