# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools 
@File    :regedit
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/7/9 上午8:48 
"""
import os
from collections import namedtuple

from volatity.mixin import run_cmd, data_handle

path = __file__
dirname = os.path.dirname(os.path.dirname(path))
vol3exe_path = os.path.join(dirname, r"assets\vol.exe")
Result = namedtuple("ScanResult", ["success", "data", "error"])


class Registry:
    def __init__(self, image_path):
        self.image_path = image_path
        self.hive_files = []

    def scan(self):
        try:
            print("生成hive")
            tem_path = os.path.join(dirname, "regedit_hives")
            if not os.path.exists(tem_path):
                os.mkdir(tem_path)
            else:
                # 获取tem_path下所有文件删除,清除上次缓存
                for file in os.listdir(tem_path):
                    if file.endswith(".hive"):
                        os.remove(os.path.join(tem_path, file))
            data, error = run_cmd(f"{vol3exe_path} -f {self.image_path} -o {tem_path} hivelist --dump")
            if data:
                files_data = data_handle(data, 3)
                self.hive_files = [os.path.join(tem_path, _[-1]) for _ in files_data]
                return Result(True, files_data, None)
            else:
                return Result(False, None, error)
        except Exception as e:
            return Result(False, None, e)

    def print_key(self, pth: str):
        data, error = run_cmd(f"{vol3exe_path} -f {self.image_path} printkey --key {pth}")
        if data:
            # data = data_handle(data, 6)
            return Result(True, data, None)
        else:
            return Result(False, None, error)


if __name__ == '__main__':
    r = Registry(r"C:\Users\11711\Desktop\browser\browser.raw")
