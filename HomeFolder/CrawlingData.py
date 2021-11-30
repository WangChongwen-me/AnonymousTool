import CrawlingData_ui
import initialize
import Filter
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem
import sys
class CrawlingData(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = CrawlingData_ui.Ui_Form()
        self.ui.setupUi(self)
        self.fullchange = True
        self.modification = True
        self.Sequence = True
        self.i = 0
        self.trans = QTranslator()
        self.filter = Filter.FilterData()
        self.ui.dataView.setContextMenuPolicy(Qt.CustomContextMenu)       #添加右键功能
        self.ui.checkFull.stateChanged.connect(self.tableFull)
        self.ui.checkModification.stateChanged.connect(self.tableModification)
        self.ui.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.checkSequence.stateChanged.connect(self.tableSequence)
        self.ui.dataView.verticalHeader().setVisible(False)

    def tableFull(self):
        if self.fullchange == True:
            self.ui.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.fullchange = False
        else:
            self.ui.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.ui.dataView.horizontalHeader().resizeSection(0, 125)
            self.ui.dataView.horizontalHeader().resizeSection(1, 125)
            self.ui.dataView.horizontalHeader().resizeSection(2, 125)
            self.ui.dataView.horizontalHeader().resizeSection(3, 125)
            self.fullchange = True
    def tableModification(self):
        if self.modification == True:
            self.ui.dataView.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.modification = False
        else:
            self.ui.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.modification = True
    def tableSequence(self):
        if self.Sequence == True:
            self.ui.dataView.verticalHeader().setVisible(True)
            self.Sequence = False
        else:
            self.ui.dataView.verticalHeader().setVisible(False)
            self.Sequence = True

    def on_dataView_customContextMenuRequested(self, pos):  # 添加右键
        m = QMenu(self)
        m.addAction(self.ui.actionCheck_All)
        m.addAction(self.ui.actionCopy)
        m.addAction(self.ui.actionKeyword_Filter)
        m.addAction(self.ui.actionClear)
        m.popup(self.ui.dataView.mapToGlobal(pos))
    @pyqtSlot(name='on_actionCopy_triggered')
    def on_actionCopy_triggered(self):
        #这里缺少一个有数据的判定
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
    @pyqtSlot(name='on_actionClear_triggered')
    def on_actionClear_triggered(self):
        pass
    @pyqtSlot(name='on_actionKeyword_Filter_triggered')
    def on_actionKeyword_Filter_triggered(self):
        res = self.filter.exec_()
    @pyqtSlot(name='on_actionCheck_All_triggered')
    def on_actionCheck_All_triggered(self):
        pass