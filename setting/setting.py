# -*- coding: UTF-8 -*-
"""
@Project :kivy_test 
@File    :setting
@IDE     :PyCharm 
@Author  :方正
@Date    :2023/3/4 12:46 
"""
import locale
import os
from typing import Optional

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivymd.app import MDApp

Debug_Mode = True
# 即assets文件夹,确定静态资源的源目录,防止用户复制库测试无法使用字体
Assets_Path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/')
# 修改全局默认中文字体
Default_Fonts_Path = os.path.join(os.path.dirname(__file__), 'assets/fonts/SourceHanSansCN-Regular.otf')


def init_global_font(app: MDApp, font_path: Optional[str] = None) -> None:
    """
    汉字初始化,可指定font_path设置全局字体
    :param app: MDapp程序主入口实例
    :param font_path: 字体路径,建议绝对路径,默认None调用思源黑体
    :return: None
    :rtype: None
    """
    # 注册免费商用的思源黑体字体
    if not font_path:
        font_path = os.path.join(Assets_Path, "fonts/SourceHanSansCN-Regular.otf")
    # 本地化字典确保kivymd的date_pickle使用中文日期
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    LabelBase.register(DEFAULT_FONT, font_path)