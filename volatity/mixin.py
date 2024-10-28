# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools 
@File    :mixin
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/7/6 下午3:01 
"""
import subprocess

from kivy.metrics import dp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


def run_cmd(exe_path: str) -> (str, str):
    print(exe_path)
    result = subprocess.run(exe_path, capture_output=True, text=True, shell=True, encoding="utf-8")
    return result.stdout, result.stderr


def data_handle(data: str, data_len: int) -> tuple:
    new_data = data.split("\n")
    return tuple(tuple(_.split("\t")) for _ in new_data if len(_.split("\t")) == data_len)


def tip_open(text: str):
    MDSnackbar(
        MDSnackbarText(
            text=text,
        ),
        y=dp(24),
        pos_hint={"center_x": 0.5},
        size_hint_x=0.8,
    ).open()
