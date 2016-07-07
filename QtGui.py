#-*-coding:utf-8-*-
__author__ = 'lixin'
from PyQt4 import QtGui,QtCore,Qt
import Work
import pyHook

class addDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(addDialog, self).__init__(parent)
        self.setWindowTitle('Add')
        self.setGeometry(810, 590, 275, 100)
        # self.setWindowFlags(Qt.Qt.WindowCloseButtonHint)
        self.label = [QtGui.QLabel() for x in xrange(3)]
        self.label[0].setText('Point_x   :    ')
        self.label[1].setText('Point_y   :    ')

        self.label[2].setText('Delay(ms) :    ')
        self.edit = [QtGui.QLineEdit() for x in xrange(3)]
        self.edit[2].setText('1000')
        self.button = [QtGui.QPushButton() for x in xrange(2)]
        self.button[0].setText('Add')
        self.button[1].setText('Cancel')
        mainLayout = QtGui.QGridLayout(self)
        for i in xrange(3):
            mainLayout.addWidget(self.label[i], i, 0)
            mainLayout.addWidget(self.edit[i], i, 1)
        mainLayout.addWidget(self.button[0], 4, 0)
        mainLayout.addWidget(self.button[1], 4, 1)
        self.setLayout(mainLayout)

        self.button[0].clicked.connect(self.add)
        self.button[1].clicked.connect(self.close)

    def add(self):
        if self.edit[0].text() == '' or self.edit[1].text() == '' or self.edit[2].text() == '':
            QtGui.QMessageBox.warning(self,'Error','Paramter incomplete!')
        else:
            Table = self.parentWidget().Table
            Work = self.parentWidget().Work
            Table.setRowCount(Table.rowCount()+1)
            Table.setItem(Table.rowCount()-1, 0, QtGui.QTableWidgetItem(self.edit[0].text()+','+self.edit[1].text()))
            Table.setItem(Table.rowCount()-1, 1, QtGui.QTableWidgetItem(self.edit[2].text()))
            Work.addPoint(int(self.edit[0].text()), int(self.edit[1].text()), Work.num, int(self.edit[2].text()))
            # print Work.point, Work.delay
            self.close()


class panel(QtGui.QWidget):
    def __init__(self, parent):
        super(panel, self).__init__(parent)
        self.initUI()
        self.Work = Work.Work()

    def initUI(self):
        self.Tableset()
        self.addDialog = addDialog(self)
        self.button = [QtGui.QPushButton() for x in xrange(2)]
        self.button[0].setText('Add')
        self.button[1].setText('Delete')
        self.button[0].clicked.connect(self.addDialog.show)
        self.button[1].clicked.connect(self.delete)


        self.mainlayout = QtGui.QGridLayout(self)
        self.mainlayout.addWidget(self.Table, 0, 0, 10, 10)
        self.mainlayout.addWidget(self.button[0], 10, 0, 1, 5)
        self.mainlayout.addWidget(self.button[1], 10, 5, 1, 5)
        self.setLayout(self.mainlayout)

    def Tableset(self):
        self.Table = QtGui.QTableWidget(0, 2)
        self.Table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.Table.setHorizontalHeaderLabels(["Point", "Delay"])
        self.Table.horizontalHeader().resizeSection(0, 235)
        self.Table.horizontalHeader().resizeSection(1, 235)
        self.Table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.Table.verticalHeader().hide()
        self.Table.setShowGrid(False)
        self.Table.setColumnCount(2)

    def delete(self):
        if self.Table.rowCount() and self.Table.selectedItems():
            num = self.Table.row(self.Table.selectedItems()[0])
            self.Table.removeRow(num)
            self.Work.delPoint(num)
            # print self.Work.point,self.Work.delay

class window(QtGui.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(710, 390, 500, 500)
        self.setWindowTitle('MouseClick')
        self.statusBar().showMessage('Ready')
        self.initUI()
        self.show()
        hm = pyHook.HookManager()
        hm.KeyDown = self.onKeyBoardEvent
        hm.HookKeyboard()

    def initUI(self):
        self.panel = panel(self)
        self.setCentralWidget(self.panel)

        beginAction = QtGui.QAction('Begin(F2)', self)
        beginAction.triggered.connect(self.panel.Work.start)

        endAction = QtGui.QAction('End(F3)', self)
        endAction.triggered.connect(self.panel.Work.end)

        aboutAction = QtGui.QAction('about', self)
        aboutAction.triggered.connect(self.about)

        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(beginAction)
        self.toolbar.addAction(endAction)
        self.toolbar.addAction(aboutAction)


    def about(self):
        QtGui.QMessageBox.about(self, 'About', "Auther : tumitumi\nE-mail:")

    def onKeyBoardEvent(self, event):
        if event.Key == 'F2':
            if not self.panel.Work.tid:
                self.panel.Work.start()
        elif event.Key == 'F3':
            if self.panel.Work.tid:
                self.panel.Work.end()