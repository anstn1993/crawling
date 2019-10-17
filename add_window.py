# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class AddWindow(object):
    def setupUi(self, addWindow):
        addWindow.setObjectName("AddWindow")
        addWindow.resize(400, 228)
        addWindow.setFixedSize(400, 228)

        self.buttonBox = QtWidgets.QDialogButtonBox(addWindow)#ok,canel버튼을 담는 버튼 박스
        self.buttonBox.setGeometry(QtCore.QRect(100, 160, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.description = QtWidgets.QLabel(addWindow)#다이얼로그 설명 글
        self.description.setGeometry(QtCore.QRect(20, 30, 361, 20))
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.description.setFont(font)
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setObjectName("description")


        self.searchText = QtWidgets.QLineEdit(addWindow)#추가할 검색어를 입력하는 editText
        self.searchText.setGeometry(QtCore.QRect(50, 80, 301, 31))
        self.searchText.setObjectName("searchText")


        self.retranslateUi(addWindow)
        self.buttonBox.accepted.connect(addWindow.accept)
        self.buttonBox.rejected.connect(addWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(addWindow)

    def retranslateUi(self, AddWindow):
        _translate = QtCore.QCoreApplication.translate
        AddWindow.setWindowTitle(_translate("AddWindow", "검색어 추가"))
        self.description.setText(_translate("AddWindow", "추가할 검색어를 입력한 후 \'ok\'버튼을 누르세요"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addWindow = QtWidgets.QDialog()
    ui = AddWindow()
    ui.setupUi(addWindow)
    addWindow.show()
    sys.exit(app.exec_())

