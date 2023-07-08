"""

"""
import sys
from ui.window import MainWindow, SysTrayWidget
from PySide6.QtWidgets import QApplication, QMenu
from PySide6.QtGui import QAction


def init_menu_bar():
    # 菜单栏
    file_menu = QMenu("文件", window)
    file_manu_action = QAction("退出", file_menu)
    file_manu_action.triggered.connect(exit_app)
    file_menu.addAction(file_manu_action)
    window.ui.menuBar.addMenu(file_menu)
    pass


def exit_app():
    app.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    init_menu_bar()
    tray = SysTrayWidget(app=app, window=window)
    window.show()
    sys.exit(app.exec())
