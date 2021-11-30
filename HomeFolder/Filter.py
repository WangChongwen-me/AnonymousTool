import Filter_ui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem
import sys
class FilterData(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Filter_ui.Ui_Filter()
        self.ui.setupUi(self)
        self.trans = QTranslator()
        self.setWindowIcon(QIcon("../img/main_icon.jpg"))
        #self.setWindowModality(Qt.ApplicationModal)