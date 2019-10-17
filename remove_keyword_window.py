# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remove_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget



class RemoveKeyWordWindow(QWidget):

    def __init__(self, keyWordList):
        super().__init__()
        self.keyWordList = keyWordList

    def setupUi(self, removeWindow):
        removeWindow.setObjectName("removeWindow")
        removeWindow.setWindowTitle("키워드 삭제")
        removeWindow.resize(816, 607)

        self.checkBoxList = []  # 체크박스 객체를 담을 리스트

        self.gridLayout = QtWidgets.QGridLayout(removeWindow)
        self.gridLayout.setObjectName("gridLayout")

        self.buttonBox = QtWidgets.QDialogButtonBox(removeWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(removeWindow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 692, 561))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.vBox = QtWidgets.QVBoxLayout()  # 체크박스 아이템을 배치할 수직 레이아웃

        self.checkBoxGroup = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.checkBoxGroup.setTitle('키워드 리스트')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.checkBoxGroup.setFont(font)
        self.checkBoxGroup.setObjectName("groupBox")
        self.checkBoxGroup.setLayout(self.setCheckBoxList(self.vBox))

        self.gridLayout_3 = QtWidgets.QGridLayout(self.checkBoxGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.checkBoxGroup, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.description = QtWidgets.QLabel(removeWindow)  # 검색어 삭제창 설명
        self.description.setText("삭제할 키워드를 체크한 후 \'ok\'버튼을 누르세요")
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.description.setFont(font)
        self.description.setObjectName("label")
        self.gridLayout.addWidget(self.description, 0, 0, 1, 1)

        self.buttonBox.accepted.connect(removeWindow.accept)#ok버튼 이벤트 리스너
        self.buttonBox.rejected.connect(removeWindow.reject)#cancel버튼 이벤트 리스너
        QtCore.QMetaObject.connectSlotsByName(removeWindow)

    @staticmethod
    def getResult(self):
        result = removeWindow.exec_()
        return (result == QtWidgets.QDialog.Accepted)

    def setCheckBoxList(self, vBox):#체크박스 셋
        for i in range(0, len(self.keyWordList)):
            checkBox = QtWidgets.QCheckBox(self.keyWordList[i][1], self.checkBoxGroup)
            self.checkBoxList.append(checkBox)
            vBox.addWidget(checkBox)  # 레이아웃에 체크박스 추가
        return vBox


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    removeWindow = QtWidgets.QDialog()
    ui = RemoveKeyWordWindow()
    ui.setupUi(removeWindow)
    removeWindow.show()
    sys.exit(app.exec_())
