# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools
@File    :regedit_screen
@IDE     :PyCharm
@Author  :方正
@Date    :2024/7/9 下午4:31
"""
import os
import time
from typing import TYPE_CHECKING
from collections import deque

import asynckivy
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from regipy.registry import RegistryHive

from setting.setting import init_global_font
from volatity.mixin import tip_open

path = __file__
dirname = os.path.dirname(os.path.dirname(path))

if TYPE_CHECKING:
    from regipy import NKRecord

kv_string = """
<RegistryScreen>:
    md_bg_color: self.theme_cls.primaryContainerColor
    
    MDBoxLayout:
        id:registry_box
        orientation: 'vertical'

        MDScrollView:
            id: registry_scroll_view
            do_scroll_x: False

            MDLabel:
                text: "请点击右下角加号按钮选择hive文件 "
                halign: "center"

    MDAnchorLayout:
        anchor_x: 'right'
        anchor_y: 'bottom'
        padding :[20,20,20,20]

        MDFabButton:
            icon: 'plus'
            pos_hint: {'right': 0.2, 'bottom': 0.2}
            on_press: root.file_manager_open()

"""


class RegistryTreeViewLabel(MDLabel, TreeViewNode):
    def __init__(self, key, **kwargs):
        super(RegistryTreeViewLabel, self).__init__(**kwargs)
        self.key = key
        self.md_bg_color = self.theme_cls.secondaryContainerColor
        self.adaptive_height = True
        self.allow_copy = True


class RegistryTreeView(TreeView):
    def __init__(self, hive, **kwargs):
        super(RegistryTreeView, self).__init__(**kwargs)
        self.hive = hive
        asynckivy.start(self.load_tree_async(self.hive.root, self.root))

    async def load_tree_async(self, key: 'NKRecord', parent_node):
        try:
            queue = deque([(key, parent_node)])
            start_time = time.time()
            while queue:
                current_key, current_parent = queue.popleft()
                node = self.add_node(RegistryTreeViewLabel(current_key, text=current_key.name), current_parent)
                for value in current_key.iter_values():
                    self.add_node(
                        RegistryTreeViewLabel(current_key,
                                              text=f"{value.name} : {value.value_type} = {str(value.value)}"),
                        node)
                await asynckivy.sleep(0)
                for subkey in current_key.iter_subkeys():
                    queue.append((subkey, node))
            end_time = time.time()
            total_time = end_time - start_time
            print(f"All nodes loaded in {total_time:.2f} seconds")
        except Exception as e:
            with open('error_log.txt', 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} "
                        f"Error : {str(e)}\n")
            tip_open("加载文件错误" + str(e))


class RegistryScreen(MDScreen):
    layout = ObjectProperty(None)
    file_manager = ObjectProperty(None)
    scroll_view = ObjectProperty(None)
    manager_open = BooleanProperty(False)
    hive_path = StringProperty("")

    @mainthread
    def initial(self, **kwargs):
        self.layout = self.ids.registry_box
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path, ext=[".hive"]
        )
        self.scroll_view = self.ids.registry_scroll_view
        return self.layout

    def init_hive(self):
        self.scroll_view.clear_widgets()
        hive = RegistryHive(self.hive_path)
        tree = RegistryTreeView(hive, hide_root=True)
        tree.height = Window.height
        tree.size_hint = 1, None
        tree.bind(minimum_height=tree.setter('height'))
        self.scroll_view.add_widget(tree)

    def file_manager_open(self, *args):
        self.file_manager.show(
            os.path.expanduser(os.path.join(dirname,"regedit_hives")))
        self.manager_open = True

    def select_path(self, path: str):
        self.hive_path = path
        self.exit_manager()
        self.init_hive()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


Builder.load_string(kv_string)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = RegistryScreen()

    def build(self):
        # 加载KV字符串
        init_global_font(self)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Silver"
        return self.screen

    def on_start(self):
        self.screen.initial()


if __name__ == '__main__':
    MainApp().run()
