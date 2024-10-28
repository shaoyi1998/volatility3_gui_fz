# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools 
@File    :pstree
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/7/16 上午11:08 
"""
import os
from collections import namedtuple

from volatity.mixin import run_cmd, data_handle

path = __file__
dirname = os.path.dirname(os.path.dirname(path))
vol3exe_path = os.path.join(dirname, r"assets\vol.exe")
Result = namedtuple("ScanResult", ["success", "data", "error"])


class TreeNode:
    def __init__(self, name, value=None, parent=None):
        self.name = name
        self.parent = parent
        self.value = value
        self.children = []


class Tree:
    def __init__(self):
        self.nodes_by_name: dict[str, TreeNode] = {}

    def add_node(self, name, value=None, parent_name=None) -> None:
        if name in self.nodes_by_name:
            raise ValueError(f"节点 {name} 已存在")

        parent = None
        if parent_name is not None:
            if parent_name not in self.nodes_by_name:
                raise ValueError(f"父节点 {parent_name} 不存在")
            parent = self.nodes_by_name[parent_name]

        node = TreeNode(name, value, parent)
        self.nodes_by_name[name] = node

        if parent is not None:
            parent.children.append(node)

    def get_node_by_name(self, name) -> TreeNode:
        if name not in self.nodes_by_name:
            raise KeyError(f"节点名 {name} 不存在")
        return self.nodes_by_name[name]


class PsTree:
    def __init__(self, image_path):
        self.image_path = image_path
        self.hive_files = []

    @staticmethod
    def data_to_tree(datas: tuple[tuple[str]]) -> Tree:
        root = Tree()
        for data in datas:
            pid, ppid = data[0], data[1]
            if not pid.startswith("*"):
                root.add_node(pid, data)
            else:
                pid = pid.split(" ")[-1]
                root.add_node(pid, data, ppid)
        return root

    def scan(self):
        try:
            data, error = run_cmd(f"{vol3exe_path} -f {self.image_path}  windows.pstree")
            if data:
                pstree_data = data_handle(data, 13)
                return Result(True, pstree_data, None)
            else:
                return Result(False, None, error)
        except Exception as e:
            return Result(False, None, e)

    def tree_data(self):
        # [1:]去除提示PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime
        # ExitTime        Audit   Cmd     Path
        return self.data_to_tree(self.scan().data[1:])


if __name__ == '__main__':
    r = PsTree(r"C:\Users\11711\Desktop\browser\browser.raw")
    result = r.data_to_tree(r.scan().data[1:])
    print(result)
