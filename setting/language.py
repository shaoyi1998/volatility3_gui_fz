# -*- coding: UTF-8 -*-
"""
@Project :volatility3_gui_fz 
@File    :language
@IDE     :PyCharm 
@Author  :方正
@Date    :2024/9/2 下午3:32 
"""
import abc


class Language(abc.ABC):
    # Title
    @property
    @abc.abstractmethod
    def title(self):
        pass

    # default 界面
    @property
    @abc.abstractmethod
    def mode(self):
        pass

    @property
    @abc.abstractmethod
    def theme_color(self):
        pass

    @property
    @abc.abstractmethod
    def default_help(self):
        pass

    # 进程界面
    @property
    @abc.abstractmethod
    def pstree(self):
        pass

    @property
    @abc.abstractmethod
    def pid(self):
        pass

    @property
    @abc.abstractmethod
    def offset(self):
        pass

    @property
    @abc.abstractmethod
    def handles(self):
        pass

    @property
    @abc.abstractmethod
    def threads(self):
        pass

    @property
    @abc.abstractmethod
    def sessionid(self):
        pass

    @property
    @abc.abstractmethod
    def wow64(self):
        pass

    # 文件界面
    @property
    @abc.abstractmethod
    def file(self):
        pass

    # #完整地址
    @property
    @abc.abstractmethod
    def full_address(self):
        pass

    # #物理地址
    @property
    @abc.abstractmethod
    def physical_address(self):
        pass

    # #文件过滤标签
    @property
    @abc.abstractmethod
    def tags(self):
        pass

    # #搜索文件
    @property
    @abc.abstractmethod
    def search_text(self):
        pass

    # 注册表界面
    @property
    @abc.abstractmethod
    def hive(self):
        pass

    # 系统服务界面
    @property
    @abc.abstractmethod
    def service(self):
        pass

    # 浏览器记录界面
    @property
    @abc.abstractmethod
    def browser(self):
        pass

    # 密码信息界面
    @property
    @abc.abstractmethod
    def password(self):
        pass

    # 网络信息界面
    @property
    @abc.abstractmethod
    def network(self):
        pass

    # 提示信息

    # #扫描失败
    @property
    @abc.abstractmethod
    def scan_fail(self):
        pass

    # #镜像未选择
    @property
    @abc.abstractmethod
    def image_no_choice(self):
        pass


class LanguageCN(Language):
    # Title
    @property
    def title(self):
        return "内存分析取证GUI(Volatility3)V1.0 作者:方正 https://fangzheng.work"

    # default 界面
    @property
    def mode(self):
        return "模式"

    @property
    def theme_color(self):
        return "主题颜色"

    @property
    def default_help(self):
        return "点击加号选择镜像文件 \n当前只有进程(异步bps算法加载) \n 文件查看dump(全量加载,默认保存程序主目录下) \n 注册表(异步bps算法加载) \n 提示:鼠标左键双击复制文本 \n 提示:语言修改后重启生效"

    # 进程界面
    @property
    def pstree(self):
        return "进程"

    # # 进程ID
    @property
    def pid(self):
        return "进程ID"

    # # 偏移量
    @property
    def offset(self):
        return "偏移量"

    # # 句柄
    @property
    def handles(self):
        return "句柄"

    # # 线程
    @property
    def threads(self):
        return "线程"

    # # 会话ID
    @property
    def sessionid(self):
        return "会话ID"

    # # 64位
    @property
    def wow64(self):
        return "WOW64"

    # 文件界面
    @property
    def file(self):
        return "文件"

    # #完整地址
    @property
    def full_address(self):
        return "完整地址"

    # #物理地址
    @property
    def physical_address(self):
        return "物理地址"

    # #文件过滤标签
    @property
    def tags(self):
        return ['图片', '文档', '压缩包', '音频', '视频', 'exe', 'web', '配置文件']

    # #搜索文件
    @property
    def search_text(self):
        return "搜索文字"

    # 注册表界面
    @property
    def hive(self):
        return "注册表"

    # 系统服务界面
    @property
    def service(self):
        return "系统服务"

    # 浏览器记录界面
    @property
    def browser(self):
        return "浏览器记录"

    # 密码信息界面
    @property
    def password(self):
        return "密码信息"

    # 网络信息界面
    @property
    def network(self):
        return "网络信息"

    # 提示信息
    # 扫描失败
    @property
    def scan_fail(self):
        return "扫描失败"

    # 镜像未选择
    @property
    def image_no_choice(self):
        return "镜像未选择"


class LanguageEN(Language):
    @property
    def title(self):
        return "Memory Analysis Forensics GUI (Volatility3) V1.0 Author: Fangzheng https://fangzheng.work"

    @property
    def mode(self):
        return "Mode"

    @property
    def theme_color(self):
        return "Theme Color"

    @property
    def default_help(self):
        return "Click the plus icon to select an image file \nCurrently only processes (asynchronous bps algorithm loading) \n File view dump (full load, default save to program main directory) \n Registry (asynchronous bps algorithm loading) \n Tip: Double-click with the left mouse button to copy text \n Tip: Language change takes effect after restart"

    @property
    def pstree(self):
        return "Processes"

    @property
    def pid(self):
        return "Process ID"

    @property
    def offset(self):
        return "Offset"

    @property
    def handles(self):
        return "Handles"

    @property
    def threads(self):
        return "Threads"

    @property
    def sessionid(self):
        return "Session ID"

    @property
    def wow64(self):
        return "WOW64"

    @property
    def file(self):
        return "File"

    @property
    def full_address(self):
        return "Full Address"

    @property
    def physical_address(self):
        return "Physical Address"

    @property
    def tags(self):
        return ['Images', 'Documents', 'Compressed', 'Audio', 'Video', 'Executable', 'Web', 'Config']

    @property
    def search_text(self):
        return "Search Text"

    @property
    def hive(self):
        return "Registry"

    @property
    def service(self):
        return "System Services"

    @property
    def browser(self):
        return "Browser History"

    @property
    def password(self):
        return "Password Information"

    @property
    def network(self):
        return "Network Information"

    @property
    def scan_fail(self):
        return "Scan Failed"

    @property
    def image_no_choice(self):
        return "Image Not Selected"


class LanguageFR(Language):
    @property
    def title(self):
        return "Interface Graphique d'Analyse Mémoire Forensics (Volatility3) V1.0 Auteur: Fangzheng https://fangzheng.work"

    @property
    def mode(self):
        return "Mode"

    @property
    def theme_color(self):
        return "Couleur du Thème"

    @property
    def default_help(self):
        return "Cliquez sur l'icône plus pour sélectionner un fichier image \nActuellement seulement les processus (chargement asynchrone bps) \n Voir les fichiers dump (chargement complet, sauvegarde par défaut dans le répertoire principal du programme) \n Registre (chargement asynchrone bps) \n Astuce: Double-cliquez avec le bouton gauche de la souris pour copier le texte \n Astuce: Le changement de langue prend effet après redémarrage"

    @property
    def pstree(self):
        return "Processus"

    @property
    def pid(self):
        return "ID de Processus"

    @property
    def offset(self):
        return "Décalage"

    @property
    def handles(self):
        return "Handles"

    @property
    def threads(self):
        return "Threads"

    @property
    def sessionid(self):
        return "ID de Session"

    @property
    def wow64(self):
        return "WOW64"

    @property
    def file(self):
        return "Fichier"

    @property
    def full_address(self):
        return "Adresse Complète"

    @property
    def physical_address(self):
        return "Adresse Physique"

    @property
    def tags(self):
        return ['Images', 'Documents', 'Compressés', 'Audio', 'Vidéo', 'Exécutable', 'Web', 'Configuration']

    @property
    def search_text(self):
        return "Rechercher du Texte"

    @property
    def hive(self):
        return "Registre"

    @property
    def service(self):
        return "Services Système"

    @property
    def browser(self):
        return "Historique du Navigateur"

    @property
    def password(self):
        return "Informations de Mot de Passe"

    @property
    def network(self):
        return "Informations Réseau"

    @property
    def scan_fail(self):
        return "Échec de l'Analyse"

    @property
    def image_no_choice(self):
        return "Image Non Sélectionnée"


class LanguageRU(Language):
    @property
    def title(self):
        return "Графический Интерфейс Анализа Памяти (Volatility3) V1.0 Автор: Fangzheng https://fangzheng.work"

    @property
    def mode(self):
        return "Режим"

    @property
    def theme_color(self):
        return "Цвет Темы"

    @property
    def default_help(self):
        return "Нажмите на значок плюса, чтобы выбрать файл образа \nВ настоящее время только процессы (асинхронная загрузка алгоритма bps) \n Просмотр файлов dump (полная загрузка, по умолчанию сохраняется в основной каталог программы) \n Регистр (асинхронная загрузка алгоритма bps) \n Совет: Двойной щелчок левой кнопкой мыши для копирования текста \n Совет: Изменение языка вступает в силу после перезагрузки"

    @property
    def pstree(self):
        return "Процессы"

    @property
    def pid(self):
        return "Идентификатор Процесса"

    @property
    def offset(self):
        return "Смещение"

    @property
    def handles(self):
        return "Handles"

    @property
    def threads(self):
        return "Потоки"

    @property
    def sessionid(self):
        return "Идентификатор Сессии"

    @property
    def wow64(self):
        return "WOW64"

    @property
    def file(self):
        return "Файл"

    @property
    def full_address(self):
        return "Полный Адрес"

    @property
    def physical_address(self):
        return "Физический Адрес"

    @property
    def tags(self):
        return ['Изображения', 'Документы', 'Сжатые', 'Аудио', 'Видео', 'Исполняемые', 'Веб', 'Конфигурация']

    @property
    def search_text(self):
        return "Поиск Текста"

    @property
    def hive(self):
        return "Реестр"

    @property
    def service(self):
        return "Системные Службы"

    @property
    def browser(self):
        return "История Браузера"

    @property
    def password(self):
        return "Информация о Пароле"

    @property
    def network(self):
        return "Сетевая Информация"

    @property
    def scan_fail(self):
        return "Ошибка Сканирования"

    @property
    def image_no_choice(self):
        return "Образ Не Выбран"


class LanguageES(Language):
    @property
    def title(self):
        return "Interfaz Gráfica de Análisis de Memoria Forense (Volatility3) V1.0 Autor: Fangzheng https://fangzheng.work"

    @property
    def mode(self):
        return "Modo"

    @property
    def theme_color(self):
        return "Color del Tema"

    @property
    def default_help(self):
        return "Haga clic en el ícono de más para seleccionar un archivo de imagen \nActualmente solo procesos (carga asíncrona del algoritmo bps) \n Vista de archivos dump (carga completa, guarda por defecto en el directorio principal del programa) \n Registro (carga asíncrona del algoritmo bps) \n Consejo: Haga doble clic con el botón izquierdo del ratón para copiar texto \n Consejo: El cambio de idioma surte efecto después de reiniciar"

    @property
    def pstree(self):
        return "Procesos"

    @property
    def pid(self):
        return "ID de Proceso"

    @property
    def offset(self):
        return "Desplazamiento"

    @property
    def handles(self):
        return "Handles"

    @property
    def threads(self):
        return "Hilos"

    @property
    def sessionid(self):
        return "ID de Sesión"

    @property
    def wow64(self):
        return "WOW64"

    @property
    def file(self):
        return "Archivo"

    @property
    def full_address(self):
        return "Dirección Completa"

    @property
    def physical_address(self):
        return "Dirección Física"

    @property
    def tags(self):
        return ['Imágenes', 'Documentos', 'Comprimidos', 'Audio', 'Video', 'Ejecutable', 'Web', 'Configuración']

    @property
    def search_text(self):
        return "Buscar Texto"

    @property
    def hive(self):
        return "Registro"

    @property
    def service(self):
        return "Servicios del Sistema"

    @property
    def browser(self):
        return "Historial del Navegador"

    @property
    def password(self):
        return "Información de Contraseña"

    @property
    def network(self):
        return "Información de Red"

    @property
    def scan_fail(self):
        return "Error de Escaneo"

    @property
    def image_no_choice(self):
        return "Imagen No Seleccionada"


class LanguageDE(Language):
    @property
    def title(self):
        return "Forensische Speicheranalyse GUI (Volatility3) V1.0 Autor: Fangzheng https://fangzheng.work"

    @property
    def mode(self):
        return "Modus"

    @property
    def theme_color(self):
        return "Themenfarbe"

    @property
    def default_help(self):
        return "Klicken Sie auf das Plus-Symbol, um eine Bilddatei auszuwählen \nDerzeit nur Prozesse (asynchrones bps-Algorithmus-Laden) \n Dateiansicht dump (vollständiges Laden, standardmäßig im Hauptverzeichnis des Programms speichern) \n Registrierung (asynchrones bps-Algorithmus-Laden) \n Tipp: Doppelklick mit der linken Maustaste zum Kopieren von Text \n Tipp: Sprachänderung tritt nach Neustart in Kraft"

    @property
    def pstree(self):
        return "Prozesse"

    @property
    def pid(self):
        return "Prozess-ID"

    @property
    def offset(self):
        return "Offset"

    @property
    def handles(self):
        return "Handles"

    @property
    def threads(self):
        return "Threads"

    @property
    def sessionid(self):
        return "Sitzungs-ID"

    @property
    def wow64(self):
        return "WOW64"

    @property
    def file(self):
        return "Datei"

    @property
    def full_address(self):
        return "Vollständige Adresse"

    @property
    def physical_address(self):
        return "Physische Adresse"

    @property
    def tags(self):
        return ['Bilder', 'Dokumente', 'Komprimiert', 'Audio', 'Video', 'Ausführbar', 'Web', 'Konfiguration']

    @property
    def search_text(self):
        return "Text suchen"

    @property
    def hive(self):
        return "Registrierung"

    @property
    def service(self):
        return "Systemdienste"

    @property
    def browser(self):
        return "Browser-Verlauf"

    @property
    def password(self):
        return "Passwortinformationen"

    @property
    def network(self):
        return "Netzwerkinformationen"

    @property
    def scan_fail(self):
        return "Scan fehlgeschlagen"

    @property
    def image_no_choice(self):
        return "Bild nicht ausgewäh"


Language_DICT = {
    "LanguageCN": LanguageCN(),
    "LanguageEN": LanguageEN(),
    "LanguageFR": LanguageFR(),
    "LanguageDE": LanguageDE(),
    "LanguageES": LanguageES(),
    "LanguageRU": LanguageRU(),
}

if __name__ == '__main__':
    LanguageCN()
    LanguageEN()
    LanguageFR()
    LanguageDE()
    LanguageES()
    LanguageRU()
