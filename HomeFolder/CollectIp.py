import CollectIp_ui
import carwlingAgencyIP
from PyQt5 import *
from PyQt5 import QtWidgets
import threading
import initialize
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem

class CollentIp(QtWidgets.QDialog):
    _ConllectIpThread = pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = CollectIp_ui.Ui_Form()
        self.ui.setupUi(self)
        self.fullchange = True
        self.i = 0
        self.ui.label.setVisible(False)
        self.ui.checkFull.stateChanged.connect(self.tableFull)
        self.ui.dataView.setContextMenuPolicy(Qt.CustomContextMenu)  # 添加右键功能

        self.CollectT = carwlingAgencyIP.startCollect()
        self.IPthread = QThread(self)
        self.CollectT.moveToThread(self.IPthread)
        self._ConllectIpThread.connect(self.CollectT.run)
        self.CollectT.filecontent.connect(self.writecontent)
        self.CollectT.filetrail.connect(self.writetrail)

    def tableFull(self):
        if self.fullchange == True:
            self.ui.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.fullchange = False
        else:
            self.ui.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.ui.dataView.horizontalHeader().resizeSection(0, 133)
            self.ui.dataView.horizontalHeader().resizeSection(1, 133)
            self.ui.dataView.horizontalHeader().resizeSection(2, 133)
            self.fullchange = True

    def on_dataView_customContextMenuRequested(self, pos):  # 添加右键
        m = QMenu(self)
        m.addAction(self.ui.actionCheck_All)
        m.addAction(self.ui.actionCopy)
        m.popup(self.ui.dataView.mapToGlobal(pos))

    @pyqtSlot(name='on_start_clicked')
    def on_start_clicked(self):
        if self.i > 2:
            QMessageBox.information(self, '提示', '请先清除原始数据~')
        else:
            os.chdir("../common")
            with open(r'proxyIP.py', 'w', encoding='utf-8') as f:
                f.write("import random\r\n")
                f.write("IPS = [\n")
                f.close()
            try:
                self.start()
            except Exception as e:
                print("意外终止",e)


    def start(self):
        if self.IPthread.isRunning():
            return
        self.IPthread.start()
        self._ConllectIpThread.emit()

    def writecontent(self,ip,port,judge):
        os.chdir("../common")
        if judge == 1:
            f = open('proxyIP.py', 'a+')
            f.write("   \'%s:%s\'," % (ip, port))
            f.write('\n')
            f.close()
            time = QDateTime.currentDateTime()  # 获取当前时间
            timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
            rowPosotion = self.ui.dataView.rowCount()
            self.ui.dataView.insertRow(rowPosotion)
            self.ui.dataView.setItem(self.i, 0, QTableWidgetItem(timedisplay))
            self.ui.dataView.setItem(self.i, 1, QTableWidgetItem("%s:%s"%(ip,port)))
            self.ui.dataView.setItem(self.i, 2, QTableWidgetItem("可用"))
            self.i = self.i+1
        elif judge == 0:
            time = QDateTime.currentDateTime()  # 获取当前时间
            timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
            rowPosotion = self.ui.dataView.rowCount()
            self.ui.dataView.insertRow(rowPosotion)
            self.ui.dataView.setItem(self.i, 0, QTableWidgetItem(timedisplay))
            self.ui.dataView.setItem(self.i, 1, QTableWidgetItem("%s:%s" % (ip, port)))
            self.ui.dataView.setItem(self.i, 2, QTableWidgetItem("不可用"))
            self.i = self.i + 1
        elif judge == 2:
            time = QDateTime.currentDateTime()  # 获取当前时间
            timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
            rowPosotion = self.ui.dataView.rowCount()
            self.ui.dataView.insertRow(rowPosotion)
            self.ui.dataView.setItem(self.i, 0, QTableWidgetItem(timedisplay))
            self.ui.dataView.setItem(self.i, 1, QTableWidgetItem("%s:%s" % (ip, port)))
            self.ui.dataView.setItem(self.i, 2, QTableWidgetItem("超时，疑似ip不可用"))
            self.i = self.i + 1

    def writetrail(self):
        os.chdir("../common")
        with open(r'proxyIP.py', 'a+', encoding='utf-8') as f:
            f.write("]\r\n")
            f.write("def random_ip(condition=False):\n")
            f.write("    if condition:\n")
            f.write("        return random.choice(IPS)\n")
            f.write("    else:\n")
            f.write("        return IPS[0]\n")
            f.close()
        self.IPthread.quit()
        self.ui.label.setVisible(True)

    @pyqtSlot(name='on_actionCheck_All_triggered')
    def on_actionCheck_All_triggered(self):
        pass

    @pyqtSlot(name='on_actionCopy_triggered')
    def on_actionCopy_triggered(self):
        if self.i > 0:
            selected_ranges = self.ui.dataView.selectedRanges()[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
            text_str = ""  # 最后总的内容
            # 行（选中的行信息读取）
            for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                row_str = ""
                # 列（选中的列信息读取）
                for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                    item = self.ui.dataView.item(row, col)
                    row_str += item.text() + '\t'  # 制表符间隔数据
                text_str += row_str + '\n'  # 换行
            clipboard = qApp.clipboard()  # 获取剪贴板
            clipboard.setText(text_str)  # 内容写入剪贴板
    def keyPressEvent(self, event):
        """ Ctrl + C复制表格内容 """
        if self.i > 0:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                # 获取表格的选中行
                selected_ranges = self.ui.dataView.selectedRanges()[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
                text_str = ""  # 最后总的内容
                # 行（选中的行信息读取）
                for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                    row_str = ""
                    # 列（选中的列信息读取）
                    for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                        item = self.ui.dataView.item(row, col)
                        row_str += item.text() + '\t'  # 制表符间隔数据
                    text_str += row_str + '\n'  # 换行
                clipboard = qApp.clipboard()  # 获取剪贴板
                clipboard.setText(text_str)  # 内容写入剪贴板