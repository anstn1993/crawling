# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets

class NotificationWindow(object):

    def __init__(self, newArticleList, dialog):
        self.newArticleList = newArticleList
        self.dialog = dialog

    def updateNewArticleList(self, newArticleList):
        self.newArticleList = newArticleList

    def setupUi(self):
        self.dialog.setObjectName("새로운 기사 알림")
        self.dialog.resize(1300, 599)
        self.gridLayout = QtWidgets.QGridLayout(self.dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableWidget(self.dialog)
        self.tableView.setObjectName("tableView")
        self.setTableWidget()
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)
        QtWidgets.QApplication.processEvents()
        QtGui.QGuiApplication.processEvents()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "새로운 기사 알림"))
        self.label.setText(_translate("Dialog", "새로운 기사가 있습니다."))

    def setTableWidget(self):
        self.tableView.setRowCount(len(self.newArticleList))
        self.tableView.setColumnCount(4)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 내용 수정 불가
        dataHeader = ['검색어', '키워드', '기사 제목', '링크']  # 헤더 아이템
        self.tableView.setHorizontalHeaderLabels(dataHeader)  # 헤더 아이템 셋
        self.tableView.itemDoubleClicked.connect(self.openURL)

        for i in range(0, len(self.newArticleList)):
            self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(self.newArticleList[i][0]))
            if self.newArticleList[i][1] == None:
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(''))
            else:
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(self.newArticleList[i][1]))
            self.tableView.setItem(i, 2, QtWidgets.QTableWidgetItem(self.newArticleList[i][2]))
            self.tableView.setItem(i, 3, QtWidgets.QTableWidgetItem(self.newArticleList[i][3]))

        self.tableView.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
        self.tableView.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
        QtWidgets.QApplication.processEvents()

    def updateTableWidget(self):
        self.tableView.setRowCount(len(self.newArticleList))
        self.tableView.setColumnCount(4)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 내용 수정 불가
        for i in range(0, len(self.newArticleList)):
            self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(self.newArticleList[i][0]))
            if self.newArticleList[i][1] == None:
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(''))
            else:
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(self.newArticleList[i][1]))
            self.tableView.setItem(i, 2, QtWidgets.QTableWidgetItem(self.newArticleList[i][2]))
            self.tableView.setItem(i, 3, QtWidgets.QTableWidgetItem(self.newArticleList[i][3]))

        self.tableView.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
        self.tableView.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
        QtWidgets.QApplication.processEvents()


    def openURL(self):
        column = self.tableView.currentItem().column()  # 클릭한 아이템의 열
        url = self.tableView.currentItem().text()  # 클릭한 아이템의 내용
        if column == 3 and url != '링크 없음':  # 링크열의 아이템을 더블클릭했고 그 아이템에 링크가 있는 경우에만 다음의 로직을 수행
            webbrowser.open(url)  # 해당 링크를 브라우저로 연다

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = NotificationWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

