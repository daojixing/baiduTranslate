#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Allow us to find shortyQt from the examples folder
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shortyQt import Shorty
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu, qApp, QMessageBox,QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication,Qt,QUrl
import sys
from PyQt5.QtWebEngineWidgets import  QWebEngineView
import re
import urllib.parse



class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self,url,*args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置窗口标题
        self.setWindowTitle('百度翻译')

        self.resize(1000, 600)
        #self.setWindowFlags()


        # 设置窗口图标
        self.setWindowIcon(QIcon(sys.path[0]+'/bd'))
        # 设置窗口大小900*600
        self.setWindowFlags( Qt.WindowCloseButtonHint
                            |Qt.Popup)
        self.show()
        # 设置浏览器
        self.browser = QWebEngineView()
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)
        self.addClipbordListener()
        self.Tranlate=False
        # self.Top=False
        self.auto_hinde=False
        # self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        # self.shortcut.activated.connect(self.on_open)

    # def on_open(self):
    #     print("Opening!")
    def goto(self,url):
        # print("isHidden()",self.isHidden())
        # print("isMinimized()", self.isMinimized())
        # print("isActiveWindow()", self.isActiveWindow())
        self.browser.setUrl(QUrl(url))
        if self.isMinimized():
            self.showNormal()
        if self.isHidden():
            self.show()
        #print(self.windowFlags())
        # if self.Top:
        #     self.setWindowFlags(Qt.WindowStaysOnTopHint)


    def addClipbordListener(self):
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.test)

    def contain_zh(self,word):
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zh_pattern.search(word)
        return match
    def test(self):
        if self.Tranlate==False:
            return
        copied_text=self.clipboard.text()
        print(copied_text)
        if self.contain_zh(copied_text):
            return
        self.goto(self.get_url(copied_text))
    def get_url(self,copyBuff):
        normalizedText = copyBuff.replace('-\n', '')
        normalizedText = normalizedText.replace('\n', ' ')
        normalizedText = normalizedText.replace('\'', '\\\'')
        normalizedText = normalizedText.replace('. ', ' ')

        text = urllib.parse.quote(normalizedText)
        text = text.replace("%0D", "")
        url = 'https://fanyi.baidu.com/#en/zh/' + text
        return url
    def leaveEvent(self, QEvent):
        if self.auto_hinde:
            self.hide()
    def mouseReleaseEvent(self, QMouseEvent):
        print('re')

    def releaseMouse(self):
        print('re')
    def mouseDoubleClickEvent(self, QMouseEvent):
        print('click')





if __name__ == '__main__':

    app = QApplication(sys.argv)

    QApplication.setQuitOnLastWindowClosed(False)



    w = MainWindow('https://fanyi.baidu.com/')

    tp = QSystemTrayIcon()
    #sys.path[0]
    tp.setIcon(QIcon(sys.path[0]+'/bd'))
    # 设置系统托盘图标的菜单
    def start():
        w.Tranlate=not w.Tranlate
        if w.Tranlate:
            tp.showMessage('百度翻译', '已经开始', icon=0)
        else:
            tp.showMessage('百度翻译', '已经暂停', icon=0)

    # def top():
    #     w.Top= not w.Top
    #     if w.Top:
    #         tp.showMessage('百度翻译', '开启置顶', icon=0)
    #     else:
    #         tp.showMessage('百度翻译', '关闭置顶', icon=0)
    # def auto_hide():
    #     w.auto_hinde=not w.auto_hinde
    #     if w.auto_hinde:
    #         tp.showMessage('百度翻译', '自动隐藏', icon=0)
    #     else:
    #         tp.showMessage('百度翻译', '不自动隐藏', icon=0)
    a1 = QAction('&开始',checkable=True, triggered=start)
    # a2 = QAction('&切换置顶', triggered=top)
    #a3=QAction('&隐藏',checkable=True,triggered=auto_hide)

    def quitApp():
        QCoreApplication.instance().quit()
        tp.setVisible(False)
    a4 = QAction('&退出', triggered=quitApp)  # 直接退出可以用qApp.quit

    tpMenu = QMenu()
    tpMenu.addAction(a1)
    # tpMenu.addAction(a2)
    #tpMenu.addAction(a3)
    tpMenu.addAction(a4)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    # 信息提示
    # 参数1：标题
    # 参数2：内容
    # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标



    def message():
        print("弹出的信息被点击了")


    tp.messageClicked.connect(message)


    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            w.show()
        # print("系统托盘的图标被点击了")


    tp.activated.connect(act)

    # sys为了调用sys.exit(0)退出程序
    # 最后,我们进入应用的主循环.事件处理从这里开始.主循环从窗口系统接收事件,分派它们到应用窗口.如果我们调用了exit()方法或者主窗口被销毁,则主循环结束.sys.exit()方法确保一个完整的退出.环境变量会被通知应用是如何结束的.
    # exec_()方法是有一个下划线的.这是因为exec在Python中是关键字.因此,用exec_()代替.
    sys.exit(app.exec_())

