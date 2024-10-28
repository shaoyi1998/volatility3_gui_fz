# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools 
@File    :file
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/7/6 下午2:58 
"""
import os
from collections import namedtuple

from volatity.mixin import run_cmd, data_handle, tip_open

path = __file__
dirname = os.path.dirname(os.path.dirname(path))
vol3exe_path = os.path.join(dirname, r"assets\vol.exe")
vol3py_path = os.path.join(dirname, r"volatility3-develop\vol.py")

Result = namedtuple("ScanResult", ["success", "data", "error"])


class File:
    def __init__(self, image_path):
        self.image_path = image_path
        self.files_table_tuple = None

    def scan(self) -> Result:
        data, error = run_cmd(f"{vol3exe_path}  -f {self.image_path} filescan")
        if data:
            files_data = data_handle(data, 3)
            self.files_table_tuple = files_data
            return Result(True, self.files_table_tuple, None)
        else:
            return Result(False, None, error)

    def dump_file(self, file_offset: str, filename: str) -> Result:
        if "\\" in filename:
            filename = filename.split("\\")[-1]
        if os.path.exists(filename):
            return False, None, "文件已存在"
        data, error = run_cmd(f"{vol3exe_path} -f {self.image_path} dumpfiles --physaddr {file_offset}")
        if data:
            out_file = data_handle(data, 4)[-1][-1]
            try:
                os.rename(out_file, filename)
                tip_open("文件dump成功,已保存在程序同目录下")
                return Result(True, data, None)
            except FileNotFoundError:
                tip_open("该文件不在镜像内存中,无法dump")
                return Result(False, data, "该文件不在镜像内存中,无法dump")
        else:
            return Result(False, None, error)


if __name__ == '__main__':
    f = File(r'C:\Users\11711\Desktop\browser\browser.raw')
    x = f.scan().data
