# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import urllib.parse

from PyQt5.QtCore import QDateTime

from bs4 import BeautifulSoup
import time
import threading
from add_window import AddWindow
from remove_window import RemoveWindow
from add_keyword_window import AddKeyWordWindow
from remove_keyword_window import RemoveKeyWordWindow
from notification_window import NotificationWindow
import sqlite3
import webbrowser
from playsound import playsound
class NotificationSignal(QtCore.QObject):#새로운 알림이 왔을때를 캐치하기 위한 알림 signal클래스
    notificationSignal = QtCore.pyqtSignal()


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, searchTextList, keyWordList, newsList, newArticleList):
        super().__init__()
        self.searchTextList = searchTextList
        self.keyWordList = keyWordList
        self.newsList = newsList
        self.newArticleList = newArticleList


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1039, 808)
        MainWindow.setMinimumSize(QtCore.QSize(0, 740))
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.updateDate = QtWidgets.QLabel(self.centralwidget)  # 최근 업데이트 날짜
        self.updateDate.setText('최근 업데이트: ' + QDateTime.currentDateTime().toString('yyyy-MM-dd, hh:mm:ss'))
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.updateDate.setFont(font)
        self.updateDate.setAlignment(QtCore.Qt.AlignCenter)
        self.updateDate.setObjectName("updateDate")
        self.gridLayout.addWidget(self.updateDate, 0, 0, 1, 1)

        self.buttonLayout = QtWidgets.QHBoxLayout()  # 새고로침, 검색어 추가, 삭제 버튼을 배치할 수평 레이아웃
        self.buttonLayout.setObjectName("buttonLayout")

        self.updateButton = QtWidgets.QPushButton(self.centralwidget)  # 새로고침 버튼
        self.updateButton.setText('새로고침')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.updateButton.setFont(font)
        self.updateButton.setObjectName("updateButton")
        self.buttonLayout.addWidget(self.updateButton)
        self.updateButton.clicked.connect(self.updateNews)  # 새로고침 클릭 이벤트

        self.addButton = QtWidgets.QPushButton(self.centralwidget)  # 검색어 추가 버튼
        self.addButton.setText('검색어 추가')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.buttonLayout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.showAddDialog)
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)  # 검색어 삭제 버튼
        self.removeButton.setText('검색어 삭제')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.removeButton.setFont(font)
        self.removeButton.setObjectName("removeButton")
        self.buttonLayout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.showRemoveDialog)

        self.addKeyWordButton = QtWidgets.QPushButton(self.centralwidget)  # 키워드 추가 버튼
        self.addKeyWordButton.setText('키워드 추가')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.addKeyWordButton.setFont(font)
        self.addKeyWordButton.setObjectName("addButton")
        self.buttonLayout.addWidget(self.addKeyWordButton)
        self.addKeyWordButton.clicked.connect(self.showAddKeyWordDialog)

        self.removeKeyWordButton = QtWidgets.QPushButton(self.centralwidget)  # 키워드 삭제 버튼
        self.removeKeyWordButton.setText('키워드 삭제')
        font = QtGui.QFont()
        font.setFamily("08서울남산체 L")
        self.removeKeyWordButton.setFont(font)
        self.removeKeyWordButton.setObjectName("removeButton")
        self.buttonLayout.addWidget(self.removeKeyWordButton)
        self.removeKeyWordButton.clicked.connect(self.showRemoveKeyWordDialog)

        self.notificationSignal = NotificationSignal()#알림 시그널 객체
        self.notificationSignal.notificationSignal.connect(self.showNotificationDialog)#알림 시그널이 emit되면 shoowNotificationDialog메소드 실행행
        self.notificationWindow = QtWidgets.QDialog()
        self.notification_window = NotificationWindow(self.newArticleList, self.notificationWindow)  # 알림 창
        self.notification_window.setupUi()


        self.add_window = AddWindow()  # 검색어 추가 창
        self.addWindwow = QtWidgets.QDialog()
        self.add_window.setupUi(self.addWindwow)

        self.remove_window = RemoveWindow(self.searchTextList)  # 검색어 삭제 창
        self.removeWindow = QtWidgets.QDialog()
        self.remove_window.setupUi(self.removeWindow)

        self.add_keyword_window = AddKeyWordWindow()  # 키워드 추가 창
        self.addKeyWordWindow = QtWidgets.QDialog()
        self.add_keyword_window.setupUi(self.addKeyWordWindow)

        self.remove_keyword_window = RemoveKeyWordWindow(self.keyWordList)  # 키워드 삭제 창
        self.removeKeyWordWindow = QtWidgets.QDialog()
        self.remove_keyword_window.setupUi(self.removeKeyWordWindow)

        self.gridLayout.addLayout(self.buttonLayout, 1, 0, 1, 1)  # 버튼 모음 레이아웃을 그리드 레이아웃에 추가

        self.contentTable = QtWidgets.QTableWidget()  # 검색 결과 데이터를 배치할 테이블 위젯
        self.setContentWidgetData(self.searchTextList, self.keyWordList)
        self.gridLayout.addWidget(self.contentTable, 2, 0, 1, 1)

        self.statusMessage = QtWidgets.QLabel(self.centralwidget)  # 인터넷 연결 오류가 발생하면 출력되는 메세지 위젯
        self.statusMessage.setText('데이터 스크랩핑 중...')
        self.statusMessage.setObjectName("statusMessage")
        self.gridLayout.addWidget(self.statusMessage, 3, 0, 1, 1)

        self.copyright = QtWidgets.QLabel('Copyright 2019. MOONSOOKIM All Rights Reserved.')
        self.copyright.setAlignment(QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.copyright, 4, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1039, 26))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowTitle('뉴스 스크랩핑')
        self.statusMessage.setStyleSheet('color:black')
        self.event = threading.Event()
        self.stopRegularThread = False  # 정기적으로 스크랩핑을 하는 스레드를 중지시키기 위한 boolean
        self.getNewsRegularlyThread = threading.Thread(target=self.getNews, args=(
            self.searchTextList, self.keyWordList))  # 뉴스를 정기적으로 가져오는 작업은 스레드를 따로 돌려서 실행
        self.getNewsRegularlyThread.setDaemon(True)  # 데몬설정을 true로 하여 프로그램이 종료되면 뉴스 기사를 가져오는 스레드도 종료되게끔 설정
        self.getNewsRegularlyThread.start()  # 스크랩핑 스레드 시작

    def setContentWidgetData(self, searchTextList, keyWordList):  # 테이블 위젯(검색 결과 데이터를 배치할 위젯) 셋 메소드
        self.contentTable.setObjectName("contentTable")
        self.contentTable.setRowCount(len(searchTextList) * len(keyWordList))  # row 수 설정
        self.contentTable.setColumnCount(4)  # column 수 설정
        self.contentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 내용 수정 불가
        dataHeader = ['검색어', '키워드', '기사 제목', '링크']  # 헤더 아이템
        self.contentTable.setHorizontalHeaderLabels(dataHeader)  # 헤더 아이템 셋
        self.contentTable.itemDoubleClicked.connect(self.openURL)


    def getNews(self, searchTextList, keyWordList):  # 뉴스 데이터를 정기적으로 스크랩핑하는 메소드

        self.newArticleList.clear()  # 새로운 기사 리스트 clear(clear하지 않으면 계속 알림 울림)

        if len(searchTextList) == 0:
            self.statusMessage.setText('검색어가 존재하지 않습니다')
            self.statusMessage.setStyleSheet('color:black')
            print("검색어가 존재하지 않습니다.")
            return

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}  # 일반 사용자가 request하는 것처럼 설정
        while True:
            self.newArticleList.clear()  # 새로운 기사 리스트 clear(clear하지 않으면 계속 알림 울림)
            print('검색어 크롤링(정기) 스레드 실행 중')
            networkException = False#인터넷 연결 오류가 발생하면 True
            self.updateDate.setText('최근 업데이트: ' + QDateTime.currentDateTime().toString('yyyy-MM-dd, hh:mm:ss'))
            self.statusMessage.setText('데이터 스크랩핑 중...')
            self.statusMessage.setStyleSheet('color:black')
            conn = sqlite3.connect('./data/crawling.db')#db와 connect
            cur = conn.cursor()
            if len(keyWordList) == 0:  # 키워드가 존재하지 않는 경우 검색어로만 검색 실시
                self.contentTable.clearContents()  # 검색 결과 컨텐츠를 모두 삭제
                self.contentTable.setRowCount(len(searchTextList))
                for i in range(0, len(searchTextList)):
                    searchText = searchTextList[i][1]#검색어
                    try:
                        url = 'https://search.naver.com/search.naver?where=news&query="{searchText}"&sm=tab_opt&sort=1&photo=0&field=1&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3At&mynews=0&refresh_start=0&related=0'.format(
                            searchText=searchText)
                        html = requests.get(url, headers=headers, timeout=5).text  # header를 함께 설정해서 url request를 해서 얻어진 값을 html이라는 변수에 저장
                        soup = BeautifulSoup(html, "html.parser")  # 데이터 추출을 하기 위해 beautifulsoup객체 선언
                        data = soup.select_one('#sp_nws1 > dl > dt > a')  # 필요한 데이터가 있는 태그로 이동
                        title = data.get('title')  # 태그의 속성에 담겨있는 데이터 추출(기사 제목)
                        href = data.get('href')  # 태그의 속성에 담겨있는 데이터 추출(기사 링크)
                        self.contentTable.setItem(i, 0, QtWidgets.QTableWidgetItem(searchText))  # 검색어 추가
                        cur.execute("select*from news where search_id = ?", (searchTextList[i][0],))
                        newsList = cur.fetchall()
                        print(newsList)
                        if newsList[0][1] == None or newsList[0][1] != title:#제목이 존재하지 않는 경우 제목을 update해준다
                            if self.stopRegularThread == True:
                                print('검색어 크롤링(정기) 스레드 중지')
                                return
                            self.contentTable.setItem(i, 2, QtWidgets.QTableWidgetItem(title))  # 기사 제목
                            self.contentTable.setItem(i, 3, QtWidgets.QTableWidgetItem(href))# 기사 링크
                            self.contentTable.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                            self.contentTable.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                            cur.execute("update news set title = ?, url = ? where search_id = ?", (title, href, searchTextList[i][0]))  # title, url update
                            conn.commit()
                            self.newArticleList.append((searchTextList[i][1], None, title, href))

                    except AttributeError:  # 검색 결과가 존재하지 않아서 soup.get함수의 값이 none인 경우
                        print('검색 결과 없음')
                        self.contentTable.setItem(i, 0, QtWidgets.QTableWidgetItem(searchText))
                        self.contentTable.setItem(i, 1, QtWidgets.QTableWidgetItem(''))
                        self.contentTable.setItem(i, 2, QtWidgets.QTableWidgetItem(''))
                        self.contentTable.setItem(i, 3, QtWidgets.QTableWidgetItem(''))
                        self.contentTable.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                        self.contentTable.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                    except requests.exceptions.ConnectionError as e:  # 인터넷 연결이 되어있지 않아서 데이터를 가져오지 못하는 경우
                        print('인터넷 연결 안 됨')
                        print(e)
                        networkException = True
                        break
                    except requests.exceptions.ReadTimeout as e:  # request timeout 오류
                        print('인터넷 연결 안 됨')
                        print(e)
                        networkException = True
                        break

                    if self.stopRegularThread == True:
                        print('검색어 크롤링(정기) 스레드 중지')
                        return



            else:#키워드가 존재하는 경우
                self.contentTable.clearContents()  # 검색 결과 컨텐츠를 모두 삭제
                self.contentTable.setRowCount(len(searchTextList)*len(keyWordList))
                for i in range(0, len(searchTextList)):
                    if networkException == True: break#인터넷 연결 오류시 반복문 탈출
                    searchText = searchTextList[i][1]  # 검색어
                    for j in range(0, len(keyWordList)):
                        keyWord = keyWordList[j][1]#키워드
                        try:
                            url = 'https://search.naver.com/search.naver?where=news&query="{searchText}"%20%2B{keyWord}&sm=tab_opt&sort=1&photo=0&field=1&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3At&mynews=0&refresh_start=0&related=0'.format(
                                searchText=searchText, keyWord=keyWord)
                            html = requests.get(url, headers=headers,
                                                timeout=5).text  # header를 함께 설정해서 url request를 해서 얻어진 값을 html이라는 변수에 저장
                            soup = BeautifulSoup(html, "html.parser")  # 데이터 추출을 하기 위해 beautifulsoup객체 선언
                            data = soup.select_one('#sp_nws1 > dl > dt > a')  # 필요한 데이터가 있는 태그로 이동
                            title = data.get('title')  # 태그의 속성에 담겨있는 데이터 추출(기사 제목)
                            href = data.get('href')  # 태그의 속성에 담겨있는 데이터 추출(기사 링크)
                            self.contentTable.setItem(len(keyWordList) * i + j, 0, QtWidgets.QTableWidgetItem(searchText))  # 검색어 추가
                            self.contentTable.setItem(len(keyWordList) * i + j, 1, QtWidgets.QTableWidgetItem(keyWord))  # 키워드 추가
                            self.contentTable.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                            self.contentTable.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                            cur.execute("select*from news where search_id = ? and keyword_id = ?", (searchTextList[i][0], keyWordList[j][0]))
                            newsList = cur.fetchall()
                            if newsList[0][1] == None or newsList[0][1] != title:#기사 데이터가 존재하지 않거나 기존 기사와 다른 경우
                                if self.stopRegularThread == True:
                                    print('검색어 크롤링(정기) 스레드 중지')
                                    return
                                print('검색 결과 존재')
                                self.contentTable.setItem(len(keyWordList) * i + j, 2, QtWidgets.QTableWidgetItem(title))  # 기사 제목
                                self.contentTable.setItem(len(keyWordList) * i + j, 3, QtWidgets.QTableWidgetItem(href))  # 기사 링크
                                self.contentTable.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                                self.contentTable.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                                #news 테이블에 데이터 insert
                                cur.execute("update news set title = ?, url = ? where search_id = ? and keyword_id = ?", (title, href, searchTextList[i][0], keyWordList[j][0]))
                                conn.commit()
                                self.newArticleList.append((searchTextList[i][1], keyWordList[j][1], title, href))#새 기사 리스트에 append

                        except AttributeError:  # 검색 결과가 존재하지 않아서 soup.get함수의 값이 none인 경우
                            print('검색 결과 없음')
                            self.contentTable.setItem(len(keyWordList) * i + j, 0, QtWidgets.QTableWidgetItem(searchText))
                            self.contentTable.setItem(len(keyWordList) * i + j, 1, QtWidgets.QTableWidgetItem(keyWord))
                            self.contentTable.setItem(len(keyWordList) * i + j, 2, QtWidgets.QTableWidgetItem(''))
                            self.contentTable.setItem(len(keyWordList) * i + j, 3, QtWidgets.QTableWidgetItem(''))
                            self.contentTable.resizeColumnsToContents()  # 열의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                            self.contentTable.resizeRowsToContents()  # 행의 사이즈를 데이터의 사이즈에 맞게 넓혀준다
                        except requests.exceptions.ConnectionError as e:  # 인터넷 연결이 되어있지 않아서 데이터를 가져오지 못하는 경우
                            print('인터넷 연결 안 됨')
                            print(e)
                            networkException = True
                            break
                        except requests.exceptions.ReadTimeout as e:  # request timeout 오류
                            print('인터넷 연결 안 됨')
                            print(e)
                            networkException = True
                            break
                        if self.stopRegularThread == True:
                            print('검색어 크롤링(정기) 스레드 중지')
                            return

            if networkException == True:
                self.statusMessage.setText('인터넷 연결을 확인하고 \'새로고침\' 버튼을 눌러주세요.')
                self.statusMessage.setStyleSheet('color:red')
            else:
                self.statusMessage.setText('스크랩핑 완료')
                self.statusMessage.setStyleSheet('color:black')

            cur.execute("select*from news")#newsList update
            self.newsList = cur.fetchall()

            # 기존 기사와 다른 기사가 존재하면 알림을 울린다.
            if len(self.newArticleList) != 0:#새로운 기사가 존재할 때만 알림
                self.notifyNewArticle()
                print("notification!")


            conn.close()#db close
            # time.sleep(1800)#30분 후 다시 스크랩핑
            print("정기 스크랩핑 대기중")
            self.event.wait(timeout=1800)

    def updateNews(self):  # 뉴스 데이터를 업데이트하는 메소드
        if self.getNewsRegularlyThread.is_alive():  # 현재 뉴스 스크랩핑(정기) 스레드가 실행중인 경우
            self.event.set()  # wait을 interrupt
            self.event = threading.Event()  # 다시 초기화하여 사용
            self.stopRegularThread = True  # 실행중인 뉴스 스크랩핑 스레드의 실행을 중지시키기 위해서 stopThread boolean을 true로 바꿔준다.
            self.getNewsRegularlyThread.join()  # 실행중인 스레드가 완전히 실행되어서 종료되기 전까지 메인 스레드를 중지시키고
            self.stopRegularThread = False  # 뉴스 스크랩핑 스레드가 완전히 중지되면 stopThread를 다시 false로 전환

        if not self.getNewsRegularlyThread.is_alive():
            self.contentTable.clearContents()  # 검색 결과 컨텐츠를 모두 삭제
            self.contentTable.setRowCount(len(self.searchTextList) * len(self.keyWordList))
            self.getNewsRegularlyThread = threading.Thread(target=self.getNews, args=(self.searchTextList, self.keyWordList))  # 한번 실행된 스레드는 재사용이 불가능하기 때문에 다시 초기화를 해준다
            self.getNewsRegularlyThread.setDaemon(True)  # 데몬설정을 true로 하여 프로그램이 종료되면 뉴스 기사를 가져오는 스레드도 종료되게끔 설정
            self.getNewsRegularlyThread.start()  # 스레드 시작
            self.updateDate.setText('최근 업데이트: ' + QDateTime.currentDateTime().toString('yyyy-MM-dd, hh:mm:ss'))

    def openURL(self):
        column = self.contentTable.currentItem().column()  # 클릭한 아이템의 열
        url = self.contentTable.currentItem().text()  # 클릭한 아이템의 내용
        if column == 3 and url != '링크 없음':  # 링크열의 아이템을 더블클릭했고 그 아이템에 링크가 있는 경우에만 다음의 로직을 수행
            webbrowser.open(url)  # 해당 링크를 브라우저로 연다

    def notifyNewArticle(self):
        self.notificationSignal.notificationSignal.emit()#알림 시그널 emit
        print("notification execute")

    def showNotificationDialog(self):#새로운 기사가 있을 때 띄울 알림 다이얼로그를 호출하는 메소드
        threading.Thread(target=self.playNotificationSound).start()
        self.notification_window.updateNewArticleList(self.newArticleList)
        self.notification_window.updateTableWidget()
        self.notificationWindow.exec_()#알림 다이얼로그 실행



    def showAddDialog(self):  # 검색어 추가 버튼을 누르면 호출되는 메소드
        addDialog = self.addWindwow.exec_()  # 검색어 추가 다이얼로그 실행
        if addDialog == self.addWindwow.Accepted:  # ok버튼을 누른 경우
            print(self.add_window.searchText.text())
            addedText = self.add_window.searchText.text()  # 검색어 입력창의 텍스트
            if addedText.strip():  # 검색어를 입력한 경우(좌우 공백 제거)
                self.addSearchText(str(addedText))  # 검색어 추가 메소드 실행
                self.add_window.searchText.setText('')
            else:  # 검색어를 입력하지 않은 경우
                QtWidgets.QMessageBox.warning(self, '검색어 추가 오류', '추가할 검색어를 입력하고 확인을 누르세요!', QtWidgets.QMessageBox.Yes)
                self.add_window.searchText.setText('')

    def showAddKeyWordDialog(self):  # 키워드 추가 버튼을 누르면 호출되는 메소드
        addKeyWordDialog = self.addKeyWordWindow.exec_()  # 키워드 추가 다이얼로그 실행
        if addKeyWordDialog == self.addKeyWordWindow.Accepted:  # ok버튼을 누른 경우
            print(self.add_keyword_window.keyWord.text())
            addedKeyWord = self.add_keyword_window.keyWord.text()  # 키워드 입력창의 텍스트
            if addedKeyWord.strip():  # 키워드를 입력한 경우(좌우 공백 제거)
                self.addKeyWord(str(addedKeyWord))  # 키워드 추가 메소드 실행
                self.add_keyword_window.keyWord.setText('')
            else:  # 검색어를 입력하지 않은 경우
                QtWidgets.QMessageBox.warning(self, '키워드 추가 오류', '추가할 키워드를 입력하고 확인을 누르세요!', QtWidgets.QMessageBox.Yes)
                self.add_keyword_window.keyWord.setText('')

    def addSearchText(self, searchText):  # 검색어 추가를 눌렀을 때 추가 조건(추가할 검색어를 입력한 상태에서 확인을 누른 경우)에 부합하면 호출되는 메소드
        print('검색어 추가 메소드 실행/', "검색어: " + searchText)
        # 기존 검색어 리스트에 입력한 검색어가 존재하는지 검사
        for i in range(0, len(self.searchTextList)):
            if searchText == self.searchTextList[i][1]:  # 입력한 검색어가 기존 리스트의 검색어와 같은 경우
                QtWidgets.QMessageBox.warning(self, '검색어 추가 오류', '이미 존재하는 검색어 입니다.', QtWidgets.QMessageBox.Yes)  # 이미 존재하는 검색어라는 경고메세지 출력
                return  # 함수 탈출

        conn = sqlite3.connect('./data/crawling.db')
        cur = conn.cursor()
        cur.execute("insert into search (search) values (?)", (searchText,))#search테이블에 검색어 추가
        conn.commit()

        cur.execute("select id from search where search = ?", (searchText,))
        search_id = cur.fetchone()[0]

        cur.execute("select*from news")
        newsList = cur.fetchall()

        cur.execute("select*from keyword")
        keyWordList = cur.fetchall()

        if len(newsList) == 0:#news데이터가 하나도 없는 경우
            if len(keyWordList) == 0:#키워드가 하나도 없는 경우
                cur.execute("insert into news (search_id) values (?)", (search_id,))#news테이블에 검색어 추가
                conn.commit()
            else: #키워드가 존재하는 경우 키워드 수만큼 추가를 해준다
                for i in range(0, len(keyWordList)):
                    cur.execute("insert into news (search_id, keyword_id) values (?)", (search_id, keyWordList[i][0]))#news테이블에 검색어 추가
                    conn.commit()

        else:#뉴스 데이터가 존재하는 경우

            if len(keyWordList) == 0:#키워드가 하나도 없는 경우
                cur.execute("insert into news (search_id) values (?)", (search_id,))#news테이블에 검색어 추가
                conn.commit()
            else:#키워드가 존재하는 경우 키워드를 포함해서 news데이터를 insert
                for i in range(0, len(keyWordList)):
                    cur.execute("insert into news (search_id, keyword_id) values (?, ?)", (search_id, keyWordList[i][0]))#search테이블에 검색어 추가
                    conn.commit()


        cur.execute("select*from search")
        self.searchTextList = cur.fetchall()#테이블의 데이터를 리스트에 update해준다.
        print(self.searchTextList)
        cur.execute("select*from news")
        self.newsList = cur.fetchall()#테이블의 데이터를 리스트에 update해준다.
        print(self.newsList)

        conn.close()

        self.remove_window = RemoveWindow(self.searchTextList)  # 검색어 삭제 창에도 검색어 리스트를 다시 넣어준다.
        self.removeWindow = QtWidgets.QDialog()
        self.remove_window.setupUi(self.removeWindow)
        # oldTitleList에도 추가를 해줘서 새로운 검색어도 비교가 가능하게 해준다.
        # for i in range(0, len(self.keyWordList)):
        #     self.oldTitleList.append(searchText + "_)(_" + self.keyWordList[i].strip() + "_)(_검색결과 없음_)(_링크없음_)(_new\n")
        # print(self.oldTitleList)
        QtWidgets.QMessageBox.about(self, '검색어 추가 완료', '추가된 검색어를 반영하기 위해서 스크랩핑을 다시 실시합니다.')
        self.updateNews()

    def addKeyWord(self, keyWord):  # 키워드 추가를 눌렀을 때 추가 조건(추가할 검색어를 입력한 상태에서 확인을 누른 경우)에 부합하면 호출되는 메소드
        print('키워드 추가 메소드 실행/', "키워드: " + keyWord)
        for i in range(0, len(self.keyWordList)):
            if keyWord == self.keyWordList[i][1]:  # 기존 키워드 리스트에 입력한 키워드가 존재하는 경우
                QtWidgets.QMessageBox.warning(self, '키워드 추가 오류', '이미 존재하는 키워드 입니다.',
                                              QtWidgets.QMessageBox.Yes)  # 이미 존재하는 검색어라는 경고메세지 출력
                return  # 함수 탈출

        conn = sqlite3.connect('./data/crawling.db')
        cur = conn.cursor()
        cur.execute("insert into keyword (keyword) values (?)", (keyWord,))  # keyword테이블에 검색어 추가
        conn.commit()
        cur.execute("select id from keyword where keyword = ?", (keyWord,))
        keyword_id = cur.fetchone()[0]
        cur.execute("select*from news")
        newsList = cur.fetchall()
        keywordNone = False
        if len(newsList) != 0:
            for i in range(0, len(newsList)):
                if newsList[i][4] == None:
                    cur.execute("update news set keyword_id = ? where id = ?", (keyword_id, newsList[i][0]))
                    conn.commit()
                    keywordNone = True

            if keywordNone == False:
                cur.execute("select*from search")
                searchList = cur.fetchall()
                for i in range(0, len(searchList)):
                    cur.execute("insert into news (search_id, keyword_id) values (?, ?)", (searchList[i][0], keyword_id))
                    conn.commit()


        cur.execute("select*from keyword")
        self.keyWordList = cur.fetchall()  # 테이블의 데이터를 리스트에 update해준다.
        print(self.keyWordList)
        cur.execute("select*from news")
        self.newsList = cur.fetchall()  # 테이블의 데이터를 리스트에 update해준다.
        print(self.newsList)
        conn.close()
        self.remove_keyword_window = RemoveWindow(self.keyWordList)  # 키워드 삭제 창
        self.removeKeyWordWindow = QtWidgets.QDialog()
        self.remove_keyword_window.setupUi(self.removeKeyWordWindow)
        QtWidgets.QMessageBox.about(self, '키워드 추가 완료', '추가된 키워드를 반영하기 위해서 스크랩핑을 다시 실시합니다.')
        self.updateNews()

    def showRemoveDialog(self):  # 검색어 삭제 버튼을 누를시 다이얼로그를 띄울 메소드
        print('검색어 삭제 다이얼로그 pop')
        removeDialog = self.removeWindow.exec_()
        if removeDialog == self.removeWindow.Accepted:  # ok버튼을 누른 경우
            self.removeSearchText(self.remove_window.checkBoxList)  # 검색어 삭제 메소드 실행

    def showRemoveKeyWordDialog(self):  # 키워드 삭제 버튼을 누를시 다이얼로그를 띄울 메소드
        print('키워드 삭제 다이얼로그 pop')
        removeDialog = self.removeKeyWordWindow.exec_()
        if removeDialog == self.removeKeyWordWindow.Accepted:  # ok버튼을 누른 경우
            self.removeKeyWord(self.remove_keyword_window.checkBoxList)  # 키워드 삭제 메소드 실행

    def removeSearchText(self, checkBoxList):  # 검색어를 삭제하는 메소드

        isChecked = False

        for i in range(0, len(checkBoxList)):
            if checkBoxList[i].isChecked():  # 체크박스에 체크가 되어있는 경우
                isChecked = True
                break

        if isChecked == False:  # 체크박스 체크 상태가 False인 경우
            QtWidgets.QMessageBox.warning(self, '검색어 삭제 오류', '삭제할 검색어를 체크한 후 \'ok\'버튼을 누르세요', QtWidgets.QMessageBox.Yes)  # 이미 존재하는 검색어라는 경고메세지 출력
            return  # 함수 탈출

        conn = sqlite3.connect('./data/crawling.db')
        cur = conn.cursor()
        for i in range(0, len(checkBoxList)):
            if checkBoxList[i].isChecked():  # 체크박스에 체그가 된 경우
                for j in range(0, len(self.searchTextList)):
                    if self.searchTextList[j][1] == checkBoxList[i].text():
                        cur.execute("delete from news where search_id = ?", (self.searchTextList[j][0],))
                        conn.commit()
                        break
                print(checkBoxList[i].text())
                cur.execute("delete from search where search = ?", (checkBoxList[i].text(),))#테이블에서 해당 검색어를 삭제
                conn.commit()


        cur.execute("select*from search")
        self.searchTextList = cur.fetchall()#검색어 리스트를 update
        cur.execute("select*from news")
        self.newsList = cur.fetchall()#뉴스 리스트를 update
        conn.close()
        print(self.searchTextList)
        print(self.newsList)
        self.remove_window = RemoveWindow(self.searchTextList)  # 검색어 삭제 다이얼로그의 검색어 리스트에 삭제된 검색어를 반영해주기 위해서 새롭게 객체 선언
        self.removeWindow = QtWidgets.QDialog()
        self.remove_window.setupUi(self.removeWindow)
        QtWidgets.QMessageBox.about(self, '검색어 삭제 완료', '삭제된 검색어를 반영하기 위해서 스크랩핑을 다시 실시합니다.')
        self.updateNews()

    def removeKeyWord(self, checkBoxList):  # 키워드를 삭제하는 메소드
        isChecked = False
        for i in range(0, len(checkBoxList)):
            if checkBoxList[i].isChecked():  # 체크박스에 체크가 되어있는 경우
                isChecked = True
                break

        if isChecked == False:  # 체크박스 체크 상태가 False인 경우
            QtWidgets.QMessageBox.warning(self, '키워드 삭제 오류', '삭제할 키워드를 체크한 후 \'ok\'버튼을 누르세요', QtWidgets.QMessageBox.Yes)  # 이미 존재하는 키워드라는 경고메세지 출력
            return  # 함수 탈출

        conn = sqlite3.connect('./data/crawling.db')
        cur = conn.cursor()
        for i in range(0, len(checkBoxList)):
            if checkBoxList[i].isChecked():  # 체크박스에 체그가 된 경우
                for j in range(0, len(self.keyWordList)):
                    if checkBoxList[i].text() == self.keyWordList[j][1]:  # 삭제하는 키워드가 제목 리스트의 검색어와 동일한 경우
                        cur.execute("delete from news where keyword_id = ?", (self.keyWordList[j][0],))#해당 키워드의 뉴스 모두 삭제
                        conn.commit()
                        break
                print(checkBoxList[i].text())
                cur.execute("delete from keyword where keyword = ?", (checkBoxList[i].text(),))  # 테이블에서 해당 검색어를 삭제
                conn.commit()
                # keyWordString = keyWordString.replace(checkBoxList[i].text() + "\n", "")  # 그 체크박스의 키워드만 스트링에서 지워주고
                # self.keyWordList.remove(checkBoxList[i].text() + "\n")  # 키워드 리스트에서도 삭제해준다.
                # oldTitleList에서도 해당 키워드를 가진 제목들을 다 지워준다.

        cur.execute("select*from keyword")
        self.keyWordList = cur.fetchall()  # 검색어 리스트를 update
        #키워드를 전부 삭제했으면 news데이터도 전부 삭제되기 때문에 다시 keyword가 없을 때의 news row를 채워넣어준다.
        if len(self.keyWordList) == 0:
            for i in range(0, len(self.searchTextList)):
                cur.execute("insert into news (search_id) values (?)", (self.searchTextList[i][0],))
                conn.commit()
        cur.execute("select*from news")
        self.newsList = cur.fetchall()  # 뉴스 리스트를 update
        conn.close()
        print(self.searchTextList)
        self.remove_keyword_window = RemoveKeyWordWindow(self.keyWordList)  # 검색어 삭제 다이얼로그의 검색어 리스트에 삭제된 검색어를 반영해주기 위해서 새롭게 객체 선언
        self.removeKeyWordWindow = QtWidgets.QDialog()
        self.remove_keyword_window.setupUi(self.removeKeyWordWindow)
        QtWidgets.QMessageBox.about(self, '키워드 삭제 완료', '삭제된 키워드를 반영하기 위해서 스크랩핑을 다시 실시합니다.')
        self.updateNews()

    def playNotificationSound(self):#알림음을 재생하는 메소드
        playsound("./data/notification.mp3")


if __name__ == "__main__":
    import sys

    conn = sqlite3.connect('./data/crawling.db')#크롤링 db
    cur = conn.cursor()
    #news테이블이 존재하지 않는다면 생성
    cur = conn.execute("create table if not exists news (id integer primary key autoincrement not null, title text, url text, search_id integer, keyword_id integer)")
    conn.commit()
    #search테이블이 존재하지 않는다면 생성
    cur = conn.execute("create table if not exists search (id integer primary key autoincrement not null, search text not null)")
    conn.commit()
    #키워드 테이블이 존재하지 않는다면 생성
    cur = conn.execute("create table if not exists keyword (id integer primary key autoincrement not null, keyword text not null)")
    conn.commit()

    cur.execute("select*from search")
    searchTextList = cur.fetchall()# 검색어를 담을 리스트
    print(searchTextList)

    cur.execute("select*from keyword")
    keyWordList = cur.fetchall()
    print(keyWordList)

    cur.execute("select*from news")
    newsList = cur.fetchall()
    print(newsList)
    conn.close()#db 종료
    newArticleList = []
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(searchTextList, keyWordList, newsList, newArticleList)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
