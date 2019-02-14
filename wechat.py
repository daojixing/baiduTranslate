#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu, qApp, QMessageBox,QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication,pyqtSignal,QThread
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import os.path






class MainWindow(QMainWindow):
    #urlsingal = pyqtSignal(str)
    #start=False
    # noinspection PyUnresolvedReferences
    def __init__(self,url,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setui(url)
        #self.urlsingal.connect()
        self.browser.page().profile().downloadRequested.connect(self._downloadRequested)

    def setui(self,url):
        self.setWindowTitle('微信')

        self.resize(1000, 600)
        #self.setWindowFlags()
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # 设置窗口图标
        cur_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(cur_path, 'timg.jpeg')
        self.setWindowIcon(QIcon(config_path))
        # 设置窗口大小900*600

        self.show()
        # 设置浏览器
        self.browser = QWebEngineView()
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)
    def goto(self,url):
        self.browser.setUrl(QUrl(url))

    def _downloadRequested(item):  # QWebEngineDownloadItem
        print('downloading to', item.path())
        item.accept()

if __name__ == '__main__':
    # pyqt窗口必须在QApplication方法中使用
    # 每一个PyQt5应用都必须创建一个应用对象.sys.argv参数是来自命令行的参数列表.Python脚本可以从shell里运行.这是我们如何控制我们的脚本运行的一种方法.
    app = QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)
    from PyQt5 import QtWidgets

    # QWidget窗口是PyQt5中所有用户界口对象的基本类.我们使用了QWidget默认的构造器.默认的构造器没有父类.一个没有父类的窗口被称为一个window.
    w = MainWindow("https://wx.qq.com/?&lang=zh")
    # show()方法将窗口显示在屏幕上.一个窗口是先在内存中被创建,然后显示在屏幕上的.
    w.show()

    # from PyQt5.QtWidgets import QSystemTrayIcon
    # from PyQt5.QtGui import QIcon
    # 在系统托盘处显示图标
    tp = QSystemTrayIcon(w)
    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(cur_path, 'timg.jpeg')
    tp.setIcon(QIcon(config_path))
    # 设置系统托盘图标的菜单
    a1 = QAction('&显示(Show)', triggered=w.show)


    def quitApp():
        QCoreApplication.instance().quit()
        # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
        # 直到你的鼠标移动到上面去后，才会消失，
        # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
        # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
        tp.setVisible(False)




    a2 = QAction('&退出(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit

    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    # 信息提示
    # 参数1：标题
    # 参数2：内容
    # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
    tp.showMessage('微信', '启动', icon=0)


    def message():
        print("弹出的信息被点击了")


    tp.messageClicked.connect(message)


    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            if w.isMinimized():
                print('mini')
                w.showNormal()
            if w.isHidden():
                w.show()
                
        # print("系统托盘的图标被点击了")


    tp.activated.connect(act)

    # sys为了调用sys.exit(0)退出程序
    # 最后,我们进入应用的主循环.事件处理从这里开始.主循环从窗口系统接收事件,分派它们到应用窗口.如果我们调用了exit()方法或者主窗口被销毁,则主循环结束.sys.exit()方法确保一个完整的退出.环境变量会被通知应用是如何结束的.
    # exec_()方法是有一个下划线的.这是因为exec在Python中是关键字.因此,用exec_()代替.
    sys.exit(app.exec_())
