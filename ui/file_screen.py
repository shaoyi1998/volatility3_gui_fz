import random

import asynckivy
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.chip import MDChip, MDChipText
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen

from setting.config import read_config_ini
from setting.language import Language_DICT, LanguageCN
from setting.setting import init_global_font
from volatity.file import File

# KV字符串定义MDScreen窗口
kv_string = '''
<FileListItem>
    pos_hint : {"center_x": .5, "center_y": .5}
    MDListItemLeadingIcon:
        icon: root.file_type

    MDListItemHeadlineText:
        text: root.file_name
        allow_copy:True

    MDListItemSupportingText:
        text: root.phy_addr
        allow_copy:True

    MDFabButton:
        style: "small"
        icon: "download"
        on_release: root.button_release()

<FileScreen>:
    md_bg_color: self.theme_cls.primaryColor

    MDBoxLayout:
        orientation: "vertical"
        spacing: "14dp"
        padding: "20dp"
        md_bg_color: app.theme_cls.backgroundColor

        MDTextField:
            id: search_field
            mode: "outlined"
            on_text: root.set_list_md_icons(self.text, True)
            md_bg_color: app.theme_cls.tertiaryContainerColor


            MDTextFieldLeadingIcon:
                icon: "magnify"

            MDTextFieldHintText:
                text: app.language.search_text

        MDBoxLayout:
            id: chip_box
            spacing: "12dp"
            adaptive_height: True

        MDRecycleView:
            id: rv
            viewclass: "FileListItem"
            key_size: "height"

            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"            
'''

FILE_TYPE_DICT = {
    "图片": {"icon": "image-outline", "extensions": frozenset({"jpg", "jpeg", "png", "gif", "bmp", "tiff"})},
    "文档": {"icon": "microsoft-office",
             "extensions": frozenset({"doc", "docx", "pdf", "txt", "rtf", "xls", "xlsx", "ppt", "pptx"})},
    "压缩包": {"icon": "zip-box-outline", "extensions": frozenset({"zip", "rar", "7z", "tar", "gz", "bz2"})},
    "音频": {"icon": "file-music", "extensions": frozenset({"mp3", "wav", "aac", "flac", "m4a"})},
    "视频": {"icon": "file-video", "extensions": frozenset({"mp4", "mkv", "avi", "mov", "wmv", "flv"})},
    "exe": {"icon": "alpha-e-box", "extensions": frozenset({"exe"})},
    "web": {"icon": "web", "extensions": frozenset({"html", "htm", "css", "js"})},
    "配置文件": {"icon": "file-cog",
                 "extensions": frozenset({"ini", "cfg", "conf", "properties", "xml", "yaml", "yml"})}
}


# 定义MDScreen类
class FileScreen(MDScreen):
    filter = ListProperty()
    all_data = ListProperty()
    language = ObjectProperty()

    def initial(self, data, file_plugin,language):
        self.language = language
        self.ids.search_field.hint_text = self.language.search_text
        self.set_filter_chips()
        self.update_file_list(data, file_plugin)

    def set_filter(self, active: bool, tag: str) -> None:
        '''Sets a list of tags for filtering icons.'''

        if active:
            self.filter.append(tag)
        else:
            self.filter.remove(tag)
        self.set_list_md_icons(self.ids.search_field.text, True)

    def set_filter_chips(self):
        '''Asynchronously creates and adds chips to the container.'''

        async def set_filter_chips():
            for i,tag in enumerate(FILE_TYPE_DICT.keys()):
                await asynckivy.sleep(0.1)
                chip = MDChip(
                    MDChipText(
                        text=self.language.tags[i],
                    ),
                    type="filter",
                    md_bg_color="#7bfff0",
                )
                chip.bind(active=lambda x, y, z=tag: self.set_filter(y, z))
                self.ids.chip_box.add_widget(chip)

        asynckivy.start(set_filter_chips())

    def set_list_md_icons(self, text="", search=False) -> None:
        self.ids.rv.data = []
        print(self.all_data)
        if self.filter:
            for data in self.all_data[1:]:
                for tag in self.filter:
                    if self.get_file_type(data.get("file_name")).lower() in FILE_TYPE_DICT.get(tag).get("extensions"):
                        if not text.strip():
                            self.ids.rv.data.append(data)
                        elif search:
                            if text in data.get("file_name"):
                                self.ids.rv.data.append(data)
                        else:
                            self.ids.rv.data.append(data)
        else:
            self.ids.rv.data.extend([_ for _ in self.all_data[1:] if text in _.get("file_name")])
        print("",self.ids.rv.data)
    def test(self):
        self.update_file_list(
            [[f"{_}", f"dfd{_}" + random.choice([".jpg", ".png", ".txt", ".zip"]), "dfdf"] for _ in range(10000)],
            File("./Target.vmem"))

    def update_file_list(self, data, file_plugin: File):
        for row in data:
            filename = self.get_filename(row[1])
            filetype_icon = self.get_file_type_icon(filename)
            self.ids.rv.data.append(
                {
                    "file_type": f"{filetype_icon}",
                    "file_name": f"{self.get_filename(filename)}",
                    "phy_addr": f"{self.language.full_address}: {row[1]},{self.language.physical_address}: {row[0]}",
                    "button_release": lambda physaddr=row[0], filename=row[1]: file_plugin.dump_file(physaddr, filename)
                }
            )
        if not self.all_data:
            self.all_data = [_ for _ in self.ids.rv.data]

    @staticmethod
    def get_filename(name):
        return name.split("\\")[-1] if "\\" in name else name

    @staticmethod
    def get_file_type(filename):
        # 定义常见的文件扩展名与类型的映射
        return filename.split('.')[-1].lower()

    def get_file_type_icon(self, filename):
        # 查找文件扩展名对应的类型
        file_extension = self.get_file_type(filename)
        for _, content_dict in FILE_TYPE_DICT.items():
            if file_extension in content_dict["extensions"]:
                return content_dict["icon"]

        # 如果没有找到对应的类型，返回"未知"
        return "help-circle-outline"


class FileListItem(MDListItem):
    file_type = StringProperty()
    file_name = StringProperty()
    phy_addr = StringProperty()
    button_release = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Builder.load_string(kv_string)

if __name__ == '__main__':
    class UnitTestApp(MDApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            init_global_font(self)
            self.screen = FileScreen()
            self.screen.language = Language_DICT.get(read_config_ini()["language"], LanguageCN())
            self.language = Language_DICT.get(read_config_ini()["language"], LanguageCN())


        def build(self):
            # 加载KV字符串
            return self.screen

        def on_start(self):

            self.screen.set_filter_chips()
            self.screen.test()


    UnitTestApp().run()
