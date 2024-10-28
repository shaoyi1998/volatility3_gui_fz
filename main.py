# -*- coding: UTF-8 -*-
"""
@Project :ctf_tools
@File    :main
@IDE     :PyCharm
@Author  :方正
@Date    :2024/7/6 下午2:58
"""
import os
import threading
from collections import Counter
from datetime import datetime
from typing import Optional

import asynckivy
from kivy.clock import mainthread, Clock
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu

from primary_palette import COLOR_DICT
from setting.config import write_config_ini, read_config_ini
from setting.language import LanguageEN, LanguageCN, Language_DICT
from setting.setting import init_global_font
from volatity.file import File
from volatity.mixin import tip_open
from volatity.pstree import PsTree
from volatity.registry import Registry

KV = '''
#:import FileScreen ui.file_screen.FileScreen
#:import RegistryScreen ui.registry_screen.RegistryScreen
#:import PstreeScreen ui.pstree_screen.PstreeScreen
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    MDBoxLayout:
        MDNavigationRail:

            id:rail
            anchor:"bottom"
            type:"labeled"


            MDNavigationRailMenuButton:
                icon: "plus"
                on_release:app.file_manager_open()

            MDNavigationRailFabButton:
                icon: "home"
                on_release :app.change_rail('default')

            MDNavigationRailItem
            
                id:pstree_rail_item
                
                on_active :app.change_rail('pstree')

                MDNavigationRailItemIcon:
                    icon: "source-branch"

                MDNavigationRailItemLabel:
                    text: app.language.pstree

            MDNavigationRailItem
        
                id:service_rail_item
                
                on_active :app.change_rail('service')

                MDNavigationRailItemIcon:
                    icon: "server"

                MDNavigationRailItemLabel:
                    text: app.language.service

            MDNavigationRailItem
            
                id:history_rail_item
                on_active :app.change_rail('history')

                MDNavigationRailItemIcon:
                    icon: "google-chrome"

                MDNavigationRailItemLabel:
                    text: app.language.browser

            MDNavigationRailItem
                
                id:network_rail_item
                on_active :app.change_rail('network')

                MDNavigationRailItemIcon:
                    icon: "router-network"

                MDNavigationRailItemLabel:
                    text: app.language.network

            MDNavigationRailItem
                
                id:file_rail_item
                
                on_active :app.change_rail('file')

                MDNavigationRailItemIcon:
                    icon: "file-eye-outline"

                MDNavigationRailItemLabel:
                    text: app.language.file

            MDNavigationRailItem
            
                id:password_rail_item
                on_active :app.change_rail('password')
                
                MDNavigationRailItemIcon:
                    icon: "lock-remove"

                MDNavigationRailItemLabel:
                    text: app.language.password
                    
            MDNavigationRailItem
            
                id:registry_rail_item
            
                on_active :app.change_rail('registry')
                
                MDNavigationRailItemIcon:
                    icon: "file-tree"

                MDNavigationRailItemLabel:
                    text: app.language.hive

        MDScreenManager:
            id:sm

            MDScreen:
                id : default
                name :"default"
                md_bg_color: self.theme_cls.secondaryContainerColor

                    
                MDLabel:
                    pos_hint: {"center_x": .5, "center_y": .3}
                    text: app.language.default_help
                    halign: "center"
                    
                MDDropDownItem:
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.open_menu(self)
            
                    MDDropDownItemText:
                        id: drop_text
                        text: app.language.theme_color
                        font_style : "Title"
                        
                MDButton:
                    style: "elevated"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    on_release: app.change_theme_style()
                    
                    MDButtonIcon:
                        icon: "theme-light-dark"
            
                    MDButtonText:
                        text: app.language.mode
                        
                MDSegmentedButton:
                    MDSegmentedButtonItem:
                        id:LanguageCN
                        on_release: app.change_language("LanguageCN")
                
                        MDSegmentButtonIcon:
                            icon: "ideogram-cjk-variant"
                
                        MDSegmentButtonLabel:
                            text: "中文"
                
                    MDSegmentedButtonItem:
                        id:LanguageEN
                        on_release: app.change_language("LanguageEN")
                        MDSegmentButtonIcon:
                            icon: "alpha-u-box-outline"
                
                        MDSegmentButtonLabel:
                            text: "English"
                
                    MDSegmentedButtonItem:
                        id:LanguageES
                        on_release: app.change_language("LanguageES")
                        MDSegmentButtonIcon:
                            icon: "alpha-e-circle-outline"
                
                        MDSegmentButtonLabel:
                            text: "Español"
                            
                    MDSegmentedButtonItem:
                        id:LanguageFR
                        on_release: app.change_language("LanguageFR")
                        MDSegmentButtonIcon:
                            icon: "alpha-f-box-outline"
                
                        MDSegmentButtonLabel:
                            text: "Français"


                    MDSegmentedButtonItem:
                        id:LanguageDE
                        on_release: app.change_language("LanguageDE")
                        MDSegmentButtonIcon:
                            icon: "alpha-d-box-outline"
                
                        MDSegmentButtonLabel:
                            text: "Deutsch"
                            
                    MDSegmentedButtonItem:
                        id:LanguageRU
                        on_release: app.change_language("LanguageRU")
                        MDSegmentButtonIcon:
                            icon: "alpha-r-box-outline"
                
                        MDSegmentButtonLabel:
                            text: "Русский"    
                                                                                                                  

            MDScreen:
                id :loading
                name:"loading"

                MDCircularProgressIndicator:
                    size_hint: None, None
                    size: "48dp", "48dp"
                    pos_hint: {'center_x': .5, 'center_y': .5}
            
            FileScreen:
                id: file
                name: "file"
            
            RegistryScreen:
                id: registry
                name: "registry"
            
            PstreeScreen:
                id:pstree
                name:"pstree"

'''


class Example(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None
        self.image = None
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.file_plugin: Optional[File] = None
        self.registry_plugin: Optional[Registry] = None
        self.screen_cache = {}
        # index,have_other
        self.rail_last_active = []

    def build(self):
        init_global_font(self)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Bisque"
        self.language = Language_DICT.get(read_config_ini()["language"], LanguageCN())
        print(self.language)
        self.title = self.language.title
        config_data = read_config_ini()
        self.theme_cls.primary_palette = config_data["color"]
        self.theme_cls.theme_style = config_data["mode"]
        Window.size = (1200, 700)
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show(
            os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):
        self.exit_manager()
        self.image = path
        tip_open(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def change_rail(self, screen_name):
        """
        kivymd2.0.1存在bug,railitem onactive 会触发两个(老的和新的),按照在列表中索引顺序触发
        此功能为个人临时适配器,收集请求处理判断
        :param screen_name:
        :return:
        """
        self.rail_last_active.append(screen_name)
        if len(self.rail_last_active) == 1:
            pass
        elif len(self.rail_last_active) != 3:
            return
        else:
            tem = Counter(self.rail_last_active)
            tem_result = None
            two_value = False
            for key, value in tem.items():
                if value == 1:
                    tem_result = key
                if value == 2:
                    two_value = True
            if two_value:
                self.rail_last_active = [tem_result]
                screen_name = tem_result
            else:
                self.rail_last_active = [screen_name]
        if screen_name == "file":
            self.file_start()
        elif screen_name == "registry":
            self.registry_start()
        elif screen_name == "pstree":
            self.pstree_start()

    def file_start(self):
        def process_file():
            self.file_plugin = File(self.image)
            result = self.file_plugin.scan()
            if result.success:
                Clock.schedule_once(
                    lambda dt: (self.update_ui("file", **{"data": result.data,
                                                          "file_plugin": self.file_plugin,
                                                          "language": self.language
                                                          })))
            else:

                with open("scan_error.log", "a+") as f:
                    f.write(f"{datetime.now()}" + str(result.error))
                tip_open(self.language.scan_fail)

        if self.screen_cache.get("file"):
            self.root.ids.sm.current = "file"
        elif self.image:
            self.root.ids.sm.current = "loading"
            threading.Thread(target=process_file).start()
        else:
            tip_open(self.language.image_no_choice)

    def registry_start(self):
        def process_registry():
            self.regedit_plugin = Registry(self.image)
            result = self.regedit_plugin.scan()
            if result.success:
                asynckivy.start(
                    self.async_update_ui("registry", **{"data": result.data,
                                                        "registry_plugin": self.registry_plugin,
                                                        "language": self.language}))
            else:
                tip_open(self.language.scan_fail)
                with open("scan_error.log", "a+") as f:
                    f.write(f"{datetime.now()}" + str(result.error))

        if self.screen_cache.get("registry"):
            self.root.ids.sm.current = "registry"
        elif self.image:
            self.root.ids.sm.current = "loading"
            threading.Thread(target=process_registry).start()
        else:
            tip_open(self.language.image_no_choice)

    def pstree_start(self):
        def process_file():
            self.pstree_plugin = PsTree(self.image)
            result = self.pstree_plugin.scan()
            if result.success:
                print("数据量", len(result.data))
                Clock.schedule_once(
                    lambda dt: (self.update_ui("pstree", **{"data": self.pstree_plugin.data_to_tree(result.data[1:]),
                                                            "language": self.language
                                                            })))
            else:
                with open("scan_error.log", "a+") as f:
                    f.write(f"{datetime.now()}" + str(result.error))
                tip_open(self.language.scan_fail)

        if self.screen_cache.get("pstree"):
            self.root.ids.sm.current = "pstree"
        elif self.image:
            self.root.ids.sm.current = "loading"
            threading.Thread(target=process_file).start()
        else:
            tip_open(self.language.image_no_choice)

    @mainthread
    def update_ui(self, screen_name, **kwargs):
        self.root.ids.get(screen_name).initial(**kwargs)
        self.switch_to_screen(screen_name)

    async def async_update_ui(self, screen_name, **kwargs):
        # RecycleView不能使用异步async_update,数量多会一定概率不一致报错
        self.root.ids.get(screen_name).initial(**kwargs)
        self.switch_to_screen(screen_name)

    @mainthread
    def switch_to_screen(self, screen_name: str):
        if screen_name not in self.screen_cache:
            self.screen_cache[screen_name] = self.root.ids.sm.get_screen(screen_name)
        self.root.ids.sm.current = screen_name
        print(f"没有缓存,切换{screen_name}")

    def open_menu(self, item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=i: self.change_color(x),
            } for i in COLOR_DICT.keys()
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def change_color(self, text_item):
        self.theme_cls.primary_palette = COLOR_DICT.get(text_item, self.theme_cls.primary_palette)
        # 利用python标准库保存颜色配置ini以便下次重载
        write_config_ini("color", self.theme_cls.primary_palette)

    def change_theme_style(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        write_config_ini("mode", self.theme_cls.theme_style)

    def change_language(self, new_lang):
        print(new_lang)
        write_config_ini("language", new_lang)

    def on_start(self):
        lang = read_config_ini()["language"]
        self.root.ids.get(lang).active = True


Example().run()
