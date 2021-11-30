import sys
import time
from main_ui import *
from CrawlingData import *
from CollectIp import *
from SearchInfomation import *
from Filter import *
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem,QShortcut

# class MoreThreadUse(QtCore.QThread):
#     update_date = QtCore.pyqtSignal(str)   # 定义信号
#     def __init__(self,):
#         super().__init__()
#         self.sign = 0
#     def run(self):
#         while True:
#             pass
#         self.update_date.emit("?")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainUi = Ui_MainWindow()
        self.mainUi.setupUi(self)
        self.Crawling = CrawlingData()  # 第一个界面
        self.Collect = CollentIp()  # 第二个界面
        self.SearchInfomation = SearchInfomation()  # 第三个界面

        self.Filter = self.Crawling.filter
        self.trans = QTranslator()
        self.mainUi.mainTab.addTab(self.Crawling,self.Crawling.windowIcon(),self.Crawling.windowTitle())
        self.mainUi.mainTab.addTab(self.Collect, self.Collect.windowIcon(), self.Collect.windowTitle())
        self.mainUi.mainTab.addTab(self.SearchInfomation, self.SearchInfomation.windowIcon(), self.SearchInfomation.windowTitle())
        # self.sendthread = MoreThreadUse()  # 线程
        # self.sendthread.update_date.connect(self.finsh_thread)
        # self.sendthread.start()

    def finsh_thread(self):
        print("线程结束")

    @pyqtSlot(name='on_actClear_triggered')
    def on_actClear_triggered(self):
        if self.mainUi.mainTab.currentIndex() == 0:
            for i in range(0, self.Collect.i):
                if self.Crawling.i >= 0:
                    print(self.Crawling.i)
                    self.Crawling.i = self.Crawling.i - 1
                    self.Crawling.ui.dataView.removeRow(self.Collect.i)
        if self.mainUi.mainTab.currentIndex() == 1:
            for i in range(0,self.Collect.i):
                if self.Collect.i >= 0:
                    print(self.Collect.i)
                    self.Collect.i = self.Collect.i - 1
                    self.Collect.ui.dataView.removeRow(self.Collect.i)
        if self.mainUi.mainTab.currentIndex() == 2:
            for i in range(0,self.SearchInfomation.i):
                if self.SearchInfomation.i >= 0:
                    print(self.SearchInfomation.i)
                    self.SearchInfomation.i = self.SearchInfomation.i - 1
                    self.SearchInfomation.ui.dataView.removeRow(self.SearchInfomation.i)
        print("clear被触发")

    @pyqtSlot(name='on_actionChinese_triggered')
    def on_actionChinese_triggered(self):
        self.trans.load("main_ui_CN")
        self.Crawling.trans.load("CrawlingData_ui_CN") #
        self.Filter.trans.load("Filter_ui_CN")  ##
        app = QApplication.instance()
        app.installTranslator(self.trans)
        app.installTranslator(self.Crawling.trans) #
        app.installTranslator(self.Filter.trans)  ##
        self.mainUi.retranslateUi(self)
        self.Crawling.ui.retranslateUi(self.Crawling) #
        self.Filter.ui.retranslateUi(self.Filter)  ##
        self.mainUi.mainTab.setTabText(0,"爬取数据") #

    @pyqtSlot(name='on_actionEnglish_triggered')
    def on_actionEnglish_triggered(self):
        self.trans.load("en")
        self.Crawling.trans.load("en") #
        self.Filter.trans.load("en")  ##
        app = QApplication.instance()
        app.installTranslator(self.trans)
        app.installTranslator(self.Crawling.trans) #
        app.installTranslator(self.Filter.trans)  ##
        self.mainUi.retranslateUi(self)
        self.Crawling.ui.retranslateUi(self.Crawling) #
        self.Filter.ui.retranslateUi(self.Filter)
        self.mainUi.mainTab.setTabText(0, "Crawling Data") #


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(QPixmap("../img/main_icon.jpg"))  # 启动程序的图片
    # 效果 fade =1 淡入   fade= 2  淡出，  t sleep 时间 毫秒
    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 30:
            newOpacity = self.windowOpacity() + 0.02  # 设置淡入
            if newOpacity > 1:
                break

            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.02)
        time.sleep(0.5)
        t = 0
        while t <= 30:
            newOpacity = self.windowOpacity() - 0.02  # 设置淡出
            if newOpacity < 0:
                break
            self.setWindowOpacity(newOpacity)
            t += 1
            time.sleep(0.02)