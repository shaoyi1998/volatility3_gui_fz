# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools 
@File    :pstree_screen
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/7/16 上午10:44 
"""
import time
from typing import TYPE_CHECKING
from collections import deque

import asynckivy
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemHeadlineText, \
    MDListItemTertiaryText
from kivymd.uix.screen import MDScreen

from setting.setting import init_global_font
from volatity.mixin import tip_open
from volatity.pstree import PsTree

if TYPE_CHECKING:
    from volatity.pstree import Tree

kv_string = """
<PstreeScreen>:
    md_bg_color: self.theme_cls.primaryContainerColor

    MDBoxLayout:
        id:registry_box
        orientation: 'vertical'

        MDScrollView:
            id: registry_scroll_view
            do_scroll_x: False

"""


class PstreeTreeViewLabel(MDLabel, TreeViewNode):
    data_lst = ListProperty()

    def __init__(self, key, **kwargs):
        super(PstreeTreeViewLabel, self).__init__(**kwargs)
        self.key = key
        # self.md_bg_color = self.theme_cls.secondaryContainerColor
        self.adaptive_height = True
        self.allow_copy = True

    def on_touch_down(self, touch):
        print(self.data_lst)
        MDDialog(
            MDDialogHeadlineText(
                text=self.text,
                halign="center",
                allow_copy=True,
            ),
            MDDialogContentContainer(
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="information-outline",
                    ),
                    MDListItemHeadlineText(
                        text=f"Pid:{self.data_lst[0].split(' ')[-1]}",
                        allow_copy=True,
                    ),
                    MDListItemSupportingText(
                        text=f"offset:{self.data_lst[3]}  Handles:{self.data_lst[5]}",
                        allow_copy=True,
                    ),
                    MDListItemTertiaryText(
                        text=f"Threads:{self.data_lst[4]} SessionId:{self.data_lst[6]} Wow64:{self.data_lst[7]}",
                        allow_copy=True,
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="clipboard-text-clock",
                    ),
                    MDListItemSupportingText(
                        text=f"start_time:{self.data_lst[8]} ",
                        allow_copy=True,
                    ),
                    MDListItemTertiaryText(
                        text=f"end_time:{self.data_lst[9]}",
                        allow_copy=True,
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="powershell",
                    ),
                    MDListItemHeadlineText(
                        text=f"Cmd:{self.data_lst[11]}",
                        allow_copy=True,
                    ),
                    MDListItemSupportingText(
                        text=f"Path:{self.data_lst[12]}",
                        allow_copy=True,
                    ),
                    MDListItemTertiaryText(
                        text=f"Audit:{self.data_lst[10]}",
                        allow_copy=True,
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                orientation="vertical",
            ),
            width_offset=dp(2)
        ).open()


class PstreeTreeView(TreeView):
    def __init__(self, datas, **kwargs):
        super(PstreeTreeView, self).__init__(**kwargs)
        asynckivy.start(self.load_tree_async(datas, self.root))

    async def load_tree_async(self, data: 'Tree', parent):
        try:
            queue = deque([(_, parent) for _ in data.nodes_by_name.values() if _.parent is None])
            start_time = time.time()
            while queue:
                treenode, parent = queue.popleft()
                parent_list = treenode.value
                node = self.add_node(PstreeTreeViewLabel(treenode.name, text=parent_list[2], data_lst=parent_list),
                                     parent)
                for child in treenode.children:
                    val_list = child.value
                    self.add_node(
                        PstreeTreeViewLabel(child.name, text=str(val_list[2]), data_lst=val_list), node)
                    if child.children:
                        for _ in child.children:
                            queue.append((_, node))
            await asynckivy.sleep(0)

            end_time = time.time()
            total_time = end_time - start_time
            print(f"All nodes loaded in {total_time:.2f} seconds")
        except Exception as e:
            with open('error_log.txt', 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} "
                        f"Error : {str(e)}\n")
            tip_open("加载文件错误" + str(e))


class PstreeScreen(MDScreen):
    image_path = StringProperty("")
    scroll_view = ObjectProperty(None)
    language = ObjectProperty()

    @mainthread
    def initial(self, data, language):
        self.language = language
        tree = PstreeTreeView(data, hide_root=True)
        tree.height = Window.height
        tree.size_hint = 1, None
        tree.bind(minimum_height=tree.setter('height'))
        self.scroll_view = self.ids.registry_scroll_view
        self.scroll_view.add_widget(tree)


Builder.load_string(kv_string)
if __name__ == '__main__':
    class UnitTestApp(MDApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.screen = PstreeScreen()

        def build(self):
            # 加载KV字符串
            init_global_font(self)
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Silver"
            return self.screen

        def on_start(self):
            r = PsTree(r"C:\Users\11711\Desktop\browser\browser.raw")
            data = r.data_to_tree(r.scan().data[1:])
            self.screen.initial(data)


    UnitTestApp().run()
