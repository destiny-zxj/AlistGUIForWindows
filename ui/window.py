"""

"""
from PySide6.QtWidgets import QMainWindow, QWidget, QSystemTrayIcon, QMenu, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon, QAction, QCloseEvent, QPixmap
from ui.MainWindow import Ui_MainWindow
from common import util, settings
from ui import app_rc
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status = -1  # -1：初始状态 0：已关闭 1：已开启 2：已就绪
        self.pid = None
        self.alist_bin = None
        self.init()
        self.check_status()

    def init(self):
        # 程序图标
        self.setWindowIcon(QIcon(settings.CONST_IMG_APP_ICON))
        # 按钮事件
        self.ui.setting_alist_btn.clicked.connect(self.on_setting_alist_click)
        self.ui.console_alist_btn_run.clicked.connect(self.on_console_alist_btn_run)
        self.ui.console_alist_btn_open.clicked.connect(self.on_console_alist_btn_open)
        self.ui.console_alist_btn_stop.clicked.connect(self.on_console_alist_btn_stop)
        self.ui.console_alist_btn_admin.clicked.connect(self.on_console_alist_btn_admin)
        # 检查 AList 程序是否存在
        self.check_alist_bin()
        # 帮助
        self.ui.help_document.clicked.connect(self.on_help_document_click)
        self.ui.help_download.clicked.connect(self.on_help_download_click)
        self.ui.help_add_storage.clicked.connect(self.on_help_add_storage_click)
        self.ui.help_webdav.clicked.connect(self.on_help_webdav_click)
        # 状态栏
        # self.ui.statusBar.showMessage("啊哈", -1)
        pass

    def on_console_alist_btn_admin(self):
        """
        `查看默认用户` 按钮事件
        :return:
        """
        code, stdout = util.run_cmd('"{0}" admin --data "{1}"'.format(self.alist_bin, settings.ALIST_DATA_DIR))
        lines = stdout.splitlines()
        username = ''
        password = ''
        for line in lines:
            username_pos = line.find('username:')
            password_pos = line.find('password:')
            if username_pos != -1:
                username = line[username_pos + 9:].strip()
            if password_pos != -1:
                password = line[password_pos + 9:].strip()
        WindowUtil.show_message_box(
            text="用户名：{0}\n密码：{1}".format(username, password),
            title="提示", icon=QMessageBox.Icon.Information
        )

    def on_console_alist_btn_stop(self):
        """
        关闭 AList

        :return:
        """
        code, stdout = util.run_cmd('"{0}" stop --data "{1}"'.format(self.alist_bin, settings.ALIST_DATA_DIR))
        if code != 0:
            return
        self.status = 0
        self.check_status()

    def on_console_alist_btn_run(self):
        """
        运行 AList

        :return:
        """
        code, stdout = util.run_cmd('"{0}" start --data "{1}"'.format(self.alist_bin, settings.ALIST_DATA_DIR))
        pid_pos = stdout.find('pid:')
        if pid_pos != -1:
            self.pid = stdout[pid_pos + 4:].strip()
        if code != 0:
            return
        self.status = 1
        self.check_status()

    def on_console_alist_btn_open(self):
        """
        打开 AList 页面

        :return:
        """
        url = settings.CONST_ALIST_URL
        port = util.get_config(settings.CONST_CONFIG_SYSTEM, settings.CONST_CONFIG_ALIST_PORT)
        util.open_url_with_browser("{0}:{1}".format(url, port))

    def on_setting_alist_click(self):
        alist_bin = WindowUtil.choose_file(self)
        if alist_bin is not None:
            util.set_config(settings.CONST_CONFIG_SYSTEM, settings.CONST_CONFIG_ALIST_BIN, alist_bin)
            self.check_alist_bin()

    def on_help_document_click(self):
        util.open_url_with_browser(self.ui.help_document.property('url'))

    def on_help_download_click(self):
        util.open_url_with_browser(self.ui.help_download.property('url'))

    def on_help_add_storage_click(self):
        util.open_url_with_browser(self.ui.help_add_storage.property('url'))

    def on_help_webdav_click(self):
        util.open_url_with_browser(self.ui.help_webdav.property('url'))

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide()

    def check_alist_bin(self):
        alist_bin = util.get_config(settings.CONST_CONFIG_SYSTEM, settings.CONST_CONFIG_ALIST_BIN)
        if util.get_platform() == 'win32' and not alist_bin.endswith('.exe'):
            alist_bin += '.exe'
            alist_bin = alist_bin.replace('/', '\\')
        if not os.path.exists(alist_bin):
            self.status = -1
            WindowUtil.show_message_box(text="未找到 AList !", title="警告")
        else:
            self.alist_bin = os.path.abspath(alist_bin)
            util.set_config(settings.CONST_CONFIG_SYSTEM, settings.CONST_CONFIG_ALIST_BIN, self.alist_bin)
            self.status = 2
        self.check_status()

    def restore(self):
        """
        重置

        :return:
        """
        self.ui.console_alist_btn_open.setEnabled(False)
        self.ui.console_alist_btn_run.setEnabled(False)
        self.ui.console_alist_btn_stop.setEnabled(False)

    def check_status(self):
        """
        检查程序状态

        :return:
        """
        pixmap_type = settings.CONST_IMG_ERROR
        status_tooltip = ''
        self.restore()
        if self.status == -1:
            self.ui.setting_alist_input.setText(None)
            pixmap_type = settings.CONST_IMG_ERROR
            status_tooltip = settings.CONST_STATUS_TXT_ERROR
            self.ui.statusBar.showMessage("AList 路径无效！", -1)
            pass
            # self.ui.setting_alist_input.setText(self.__alist_bin)
        elif self.status == 0:
            pixmap_type = settings.CONST_IMG_STOP
            status_tooltip = settings.CONST_STATUS_TXT_STOP
            self.ui.console_alist_btn_run.setEnabled(True)
            self.ui.statusBar.showMessage("AList 已停止运行！", 2000)
            pass
        elif self.status == 1:
            pixmap_type = settings.CONST_IMG_RUNNING
            status_tooltip = settings.CONST_STATUS_TXT_RUNNING
            self.ui.console_alist_btn_open.setEnabled(True)
            self.ui.console_alist_btn_stop.setEnabled(True)
            status_bar_msg = "AList 正在运行..."
            if self.pid is not None:
                status_bar_msg = "AList 正在运行[PID:{0}]...".format(self.pid)
            self.ui.statusBar.showMessage(status_bar_msg, -1)
            pass
        elif self.status == 2:
            pixmap_type = settings.CONST_IMG_READY
            status_tooltip = settings.CONST_STATUS_TXT_READY
            self.ui.console_alist_btn_run.setEnabled(True)
            self.ui.console_alist_btn_admin.setEnabled(True)
            self.ui.statusBar.showMessage("AList 已准备就绪！", -1)
            pass
        # alist 路径显示
        if self.status != -1:
            self.ui.setting_alist_input.setText(self.alist_bin)
        # AList 状态
        self.ui.console_alist_status_img.setScaledContents(True)
        self.ui.console_alist_status_img.setToolTip(status_tooltip)
        pixmap = QPixmap(pixmap_type)
        pixmap.scaled(self.ui.console_alist_status_img.size())
        self.ui.console_alist_status_img.setPixmap(pixmap)


class SysTrayWidget(QWidget):

    def __init__(self, app=None, window=None):
        QWidget.__init__(self)  # 必须调用
        self.__app = app
        self.__window = window

        # 配置系统托盘
        self.__tray_icon = QSystemTrayIcon(self)
        self.__tray_icon.setIcon(QIcon(settings.CONST_IMG_APP_ICON))
        self.__tray_icon.activated.connect(self.on_activate_tray_icon)

        # 创建托盘的右键菜单
        self.__tray_menu = QMenu(self)
        # self.__tray_menu.mouseDoubleClickEvent(self.test)
        self.__tray_action = []
        self.add_tray_menu_action('PyAList', self.show_user_interface, icon=QIcon(settings.CONST_IMG_APP_ICON))
        self.__tray_menu.addSeparator()
        # self.add_tray_menu_action('显示主界面', self.show_user_interface)
        self.add_tray_menu_action('最小化到托盘', self.hide_user_interface)
        self.__tray_menu.addSeparator()
        self.add_tray_menu_action('退出', self.quit)

        # 配置菜单并显示托盘
        self.__tray_icon.setContextMenu(self.__tray_menu)  # 把tpMenu设定为托盘的右键菜单
        self.__tray_icon.setToolTip('PyAList [YCST]')  # [bug] 不显示
        self.__tray_icon.show()  # 显示托盘

    def on_activate_tray_icon(self, reason):
        # 单击左键或中键显示程序界面
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.__window.showNormal()

    def add_tray_menu_action(self, text='empty', callback=None, icon=None):
        """
        添加托盘菜单动作

        :param icon:
        :param text:
        :param callback: 回调函数
        :return:
        """
        a = QAction(text, self)
        if callback is not None:
            a.triggered.connect(callback)
        if icon is not None:
            a.setIcon(icon)
        self.__tray_menu.addAction(a)
        self.__tray_action.append(a)

    def quit(self):
        """
        退出主程序

        :return:
        """
        # print(self.__window.alist_bin, self.__window.status)
        if self.__window.alist_bin is not None and self.__window.status == 1:
            util.run_cmd("{0} stop".format(self.__window.alist_bin))
        self.__app.exit()

    def show_user_interface(self):
        """
        显示程序主窗口

        :return:
        """
        if self.__window.isMinimized():
            self.__window.showNormal()
        elif self.__window.isMaximized():
            self.__window.showMaximized()
        else:
            self.__window.show()

    def hide_user_interface(self):
        """
        隐藏程序主窗口

        :return:
        """
        self.__window.hide()


class WindowUtil:

    @staticmethod
    def show_message_box(text: str, title='警告', icon: QMessageBox.Icon = QMessageBox.Icon.Warning, buttons: list = None) -> int:
        """
        弹出消息框

        :param text: 消息内容
        :param title: 窗口标题
        :param icon: 图标
        :param buttons: 按钮列表 [{'button': '确定', 'role': QMessageBox.ButtonRole.YesRole}, ...]
        :return: 按钮代码
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        if buttons is None or len(buttons) == 0:
            msg_box.addButton('确定', QMessageBox.ButtonRole.YesRole)
        else:
            for i in range(len(buttons)):
                button = buttons[i]
                print(button)
                msg_box.addButton(button['button'], button['role'])
        if icon is not None:
            msg_box.setIcon(icon)
        else:
            msg_box.setIcon(QMessageBox.Icon.Critical)
        return msg_box.exec()

    @staticmethod
    def choose_file(parent=None):
        """
        选择文件

        :param parent: 父窗口
        :return:
        """
        filename, _ = QFileDialog.getOpenFileName(
            parent,
            caption="选择 AList 程序",
            dir=settings.BASE_DIR,
            filter="AList (*.exe)"
        )
        if filename is not None and filename != '':
            return filename
        return None
