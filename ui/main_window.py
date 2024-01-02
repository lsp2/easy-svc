from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt as qtc

from ui.ui_unframewindow import Ui_Unframewindow

#主窗口

class MainWindow(Ui_Unframewindow, QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(None,qtc.FramelessWindowHint)
        self.setupUi(self)

    #下面定义一些函数控制交互